from gym.envs import registration
from nle.minihack import MiniHackNavigation
from nle.minihack.envs.corridor import NAVIGATE_ACTIONS
from nle.minihack.reward_manager import RewardManager
from nle.nethack import Command

EAT_ACTION = Command.EAT
ACTIONS = tuple(list(NAVIGATE_ACTIONS) + [EAT_ACTION])


class MiniHackExploreMaze(MiniHackNavigation):
    """Environment for a memory challenge."""

    def __init__(self, *args, des_file, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 500)
        kwargs["actions"] = ACTIONS
        kwargs["allow_all_yn_questions"] = True
        reward_manager = RewardManager()
        reward_manager.add_eat_event(
            "apple",
            reward=0.5,
            repeatable=True,
            terminal_required=False,
            terminal_sufficient=False,
        )
        # Will never be achieved, but insures the environment keeps running
        reward_manager.add_message_event(
            ["Mission Complete."], terminal_required=True, terminal_sufficient=True
        )
        super().__init__(
            *args,
            des_file=des_file,
            reward_manager=reward_manager,
            penalty_time=-0.001,  # ensures motivation to finish level quickly
            **kwargs,
        )


class MiniHackExploreMazeEasy(MiniHackExploreMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="exploremazeeasy.des", **kwargs)


class MiniHackExploreMazeHard(MiniHackExploreMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="exploremazehard.des", **kwargs)


registration.register(
    id="MiniHack-ExploreMaze-Easy-v0",
    entry_point="nle.minihack.envs.exploremaze:MiniHackExploreMazeEasy",
)
registration.register(
    id="MiniHack-ExploreMaze-Hard-v0",
    entry_point="nle.minihack.envs.exploremaze:MiniHackExploreMazeHard",
)
