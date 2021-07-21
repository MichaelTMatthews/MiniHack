#!/usr/bin/env python
#
# Copyright (c) Facebook, Inc. and its affiliates.
import argparse
import ast
import contextlib
import random
import os
import termios
import time
import timeit
import tty
import torch

import gym
from omegaconf import OmegaConf

import nle  # noqa: F401
from nle import nethack
import nle.agent.polybeast.models
from nle.agent.polybeast import polyhydra

_ACTIONS = tuple(
    [nethack.MiscAction.MORE]
    + list(nethack.CompassDirection)
    + list(nethack.CompassDirectionLonger)
)


@contextlib.contextmanager
def dummy_context():
    yield None


@contextlib.contextmanager
def no_echo():
    tt = termios.tcgetattr(0)
    try:
        tty.setraw(0)
        yield
    finally:
        termios.tcsetattr(0, termios.TCSAFLUSH, tt)


def get_action(env, action_mode, is_raw_env, pretrained_model, obs, hidden, done):
    if action_mode == "random":
        if not is_raw_env:
            action = env.action_space.sample()
        else:
            action = random.choice(_ACTIONS)
    elif action_mode == "human":
        while True:
            with no_echo():
                ch = ord(os.read(0, 1))
            if ch == nethack.C("c"):
                print("Received exit code {}. Aborting.".format(ch))
                return None
            try:
                if is_raw_env:
                    action = ch
                else:
                    action = env._actions.index(ch)
                break
            except ValueError:
                print(
                    ("Selected action '%s' is not in action list. Please try again.")
                    % chr(ch)
                )
                continue
    elif action_mode == "pretrained":
        if not is_raw_env:
            with torch.no_grad():
                for key in obs.keys():
                    shape = obs[key].shape
                    obs[key] = torch.Tensor(obs[key].reshape((1, 1, *shape)))

                obs["done"] = torch.BoolTensor([done])

                out, hidden = pretrained_model(obs, hidden)

                action = out["action"]
        else:
            raise NotImplementedError()
            # action = random.choice(_ACTIONS)
        input()
    return action, hidden


def load_model(env, pretrained_path, pretrained_config_path):
    flags = OmegaConf.load(pretrained_config_path)
    flags["env"] = env
    flags = polyhydra.get_common_flags(flags)
    flags = polyhydra.get_environment_flags(flags)
    flags = polyhydra.get_learner_flags(flags)
    model = nle.agent.polybeast.models.create_model(flags, torch.device("cpu"))

    checkpoint_states = torch.load(pretrained_path, map_location=torch.device("cpu"))

    model.load_state_dict(checkpoint_states["model_state_dict"])

    hidden = model.initial_state(batch_size=1)
    return model, hidden


def play(
    env,
    mode,
    ngames,
    max_steps,
    seeds,
    savedir,
    no_render,
    render_mode,
    debug,
    agent_env,
    pretrained_path,
    pretrained_config_path,
):
    env_name = env
    is_raw_env = env_name == "raw"

    if is_raw_env:
        if savedir is not None:
            os.makedirs(savedir, exist_ok=True)
            ttyrec = os.path.join(savedir, "nle.ttyrec.bz2")
        else:
            ttyrec = "/dev/null"
        env = nethack.Nethack(ttyrec=ttyrec)
    else:
        env = gym.make(
            env_name,
            savedir=savedir,
            max_episode_steps=max_steps,
            observation_keys=[
                "glyphs",
                "chars",
                "colors",
                "specials",
                "blstats",
                "message",
            ],
        )
        if seeds is not None:
            env.seed(seeds)
        if not no_render:
            print("Available actions:", env._actions)

    obs = env.reset()
    done = False

    pretrained_model = None
    hidden = None
    if mode == "pretrained":
        pretrained_model, hidden = load_model(
            agent_env, pretrained_path, pretrained_config_path
        )

    steps = 0
    episodes = 0
    reward = 0.0
    action = None

    mean_sps = 0
    mean_reward = 0.0

    total_start_time = timeit.default_timer()
    start_time = total_start_time
    while True:
        if not no_render:
            if not is_raw_env:
                print("Previous reward:", reward)
                if action is not None:
                    print("Previous action: %s" % repr(env._actions[action]))
                env.render(render_mode)
            else:
                print("Previous action:", action)
                _, chars, _, _, blstats, message, *_ = obs
                msg = bytes(message)
                print(msg[: msg.index(b"\0")])
                for line in chars:
                    print(line.tobytes().decode("utf-8"))
                print(blstats)

        action, hidden = get_action(
            env, mode, is_raw_env, pretrained_model, obs, hidden, done
        )
        if action is None:
            break

        if is_raw_env:
            obs, done = env.step(action)
        else:
            obs, reward, done, info = env.step(action)
        steps += 1

        if is_raw_env:
            done = done or steps >= max_steps  # NLE does this by default.
        else:
            mean_reward += (reward - mean_reward) / steps

        if not done:
            continue

        time_delta = timeit.default_timer() - start_time

        if not is_raw_env:
            print("Final reward:", reward)
            print("End status:", info["end_status"].name)
            print("Mean reward:", mean_reward)
            print("Total reward:", mean_reward * steps)

        sps = steps / time_delta
        print("Episode: %i. Steps: %i. SPS: %f" % (episodes, steps, sps))

        episodes += 1
        mean_sps += (sps - mean_sps) / episodes

        start_time = timeit.default_timer()

        steps = 0
        mean_reward = 0.0

        if episodes == ngames:
            break
        env.reset()
    env.close()
    print(
        "Finished after %i episodes and %f seconds. Mean sps: %f"
        % (episodes, timeit.default_timer() - total_start_time, mean_sps)
    )


def main():
    parser = argparse.ArgumentParser(description="NLE Play tool.")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enables debug mode, which will drop stack into "
        "an ipdb shell if an exception is raised.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="human",
        choices=["human", "random", "pretrained"],
        help="Control mode. Defaults to 'human'.",
    )
    parser.add_argument(
        "-e",
        "--env",
        type=str,
        default="NetHackScore-v0",
        help="Gym environment spec. Defaults to 'NetHackStaircase-v0'.",
    )
    parser.add_argument(
        "--agent_env",
        type=str,
        default="",
        help="Agent name for environment.  Must correspond to "
        + "environment agent was trained in.  Only required for "
        + "--mode pretrained.",
    )
    parser.add_argument(
        "--pretrained_path",
        type=str,
        default="",
        help="Path to checkpoint to load pretrained model.",
    )
    parser.add_argument(
        "--pretrained_config_path",
        type=str,
        default="",
        help="Path to config for pretrained model.",
    )
    parser.add_argument(
        "-n",
        "--ngames",
        type=int,
        default=1,
        help="Number of games to be played before exiting. "
        "NetHack will auto-restart if > 1.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=10000,
        help="Number of maximum steps per episode.",
    )
    parser.add_argument(
        "--seeds",
        default=None,
        help="Seeds to send to NetHack. Can be a dict or int. "
        "Defaults to None (no seeding).",
    )
    parser.add_argument(
        "--savedir",
        default="nle_data/play_data",
        help="Directory path where data will be saved. "
        "Defaults to 'nle_data/play_data'.",
    )
    parser.add_argument(
        "--no-render", action="store_true", help="Disables env.render()."
    )
    parser.add_argument(
        "--render_mode",
        type=str,
        default="human",
        choices=["human", "full", "ansi"],
        help="Render mode. Defaults to 'human'.",
    )
    flags = parser.parse_args()

    if flags.debug:
        import ipdb

        cm = ipdb.launch_ipdb_on_exception
    else:
        cm = dummy_context

    with cm():
        if flags.seeds is not None:
            # to handle both int and dicts
            flags.seeds = ast.literal_eval(flags.seeds)

        if flags.savedir == "args":
            flags.savedir = "{}_{}_{}.zip".format(
                time.strftime("%Y%m%d-%H%M%S"), flags.mode, flags.env
            )

        play(**vars(flags))


if __name__ == "__main__":
    main()
