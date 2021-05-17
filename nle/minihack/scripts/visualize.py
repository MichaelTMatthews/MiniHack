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

import gym

import nle  # noqa: F401
from nle import nethack

import curses
from nle.minihack.scripts import culour


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


def get_action(env, action_mode, is_raw_env):
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
    return action


def play(env, mode, ngames, max_steps, seeds, savedir, no_render, render_mode, debug, stdscr):
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
        env = gym.make(env_name, savedir=savedir, max_episode_steps=max_steps)
        if seeds is not None:
            env.seed(seeds)
        # if not no_render:
            # print("Available actions:", env._actions)

    obs = env.reset()

    action = None

    # TODO
    k = 0
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    cols = 0
    rows = 0
    while (k != ord('q')):
        # Refresh the screen
        stdscr.refresh()

        if not no_render:
            if not is_raw_env:
                render = env.get_render(render_mode, (8, 34, 17, 45), False)

                for i, row in enumerate(render.split("\n")):
                    # stdscr.addstr(i, 0, row, curses.color_pair(1))
                    culour.addstr(stdscr, 1 + rows * 10 + i, cols * 12, row)
            else:
                _, chars, _, _, blstats, message, *_ = obs
                msg = bytes(message)
                print(msg[: msg.index(b"\0")])
                for line in chars:
                    print(line.tobytes().decode("utf-8"))
                print(blstats)

        action = get_action(env, mode, is_raw_env)
        if action is None:
            break

        if is_raw_env:
            obs, done = env.step(action)
        else:
            obs, reward, done, info = env.step(action)

        env.reset()

        cols += 1
        if cols % 5 == 0:
            cols = 0
            rows += 1

        # Wait for next input
        k = stdscr.getch()
    env.close()

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
        choices=["human", "random"],
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

        curses.wrapper(lambda x: play(**vars(flags), stdscr=x))


if __name__ == "__main__":
    main()
