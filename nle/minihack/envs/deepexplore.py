from gym.envs import registration
from nle.minihack import MiniHackNavigation
from nle.minihack.envs.corridor import NAVIGATE_ACTIONS
from nle.minihack.reward_manager import RewardManager
from nle.nethack import Command

EAT_ACTION = Command.EAT
ACTIONS = tuple(list(NAVIGATE_ACTIONS) + [EAT_ACTION])


class MiniHackDeepExplore(MiniHackNavigation):
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


class MiniHackDeepExplore2(MiniHackDeepExplore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="deepexplore2.des", **kwargs)


class MiniHackDeepExplore3(MiniHackDeepExplore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="deepexplore3.des", **kwargs)


class MiniHackDeepExplore5(MiniHackDeepExplore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="deepexplore5.des", **kwargs)


class MiniHackDeepExplore8(MiniHackDeepExplore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="deepexplore8.des", **kwargs)


class MiniHackDeepExplore10(MiniHackDeepExplore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="deepexplore10.des", **kwargs)


registration.register(
    id="MiniHack-DeepExplore-R2-v0",
    entry_point="nle.minihack.envs.deepexplore:MiniHackDeepExplore2",
)
registration.register(
    id="MiniHack-DeepExplore-R3-v0",
    entry_point="nle.minihack.envs.deepexplore:MiniHackDeepExplore3",
)
registration.register(
    id="MiniHack-DeepExplore-R5-v0",
    entry_point="nle.minihack.envs.deepexplore:MiniHackDeepExplore5",
)
registration.register(
    id="MiniHack-DeepExplore-R8-v0",
    entry_point="nle.minihack.envs.deepexplore:MiniHackDeepExplore8",
)
registration.register(
    id="MiniHack-DeepExplore-R10-v0",
    entry_point="nle.minihack.envs.deepexplore:MiniHackDeepExplore10",
)
