from nle.minihack import MiniHackNavigation
from gym.envs import registration


class MiniHackHideAndSeekMapped(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 200)
        super().__init__(*args, des_file="hidenseek_mapped.des", **kwargs)


class MiniHackHideAndSeek(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 200)
        super().__init__(*args, des_file="hidenseek.des", **kwargs)


registration.register(
    id="MiniHack-HnS-Mapped-v0",
    entry_point="nle.minihack.envs.hidenseek:MiniHackHideAndSeekMapped",
)

registration.register(
    id="MiniHack-HnS-v0",
    entry_point="nle.minihack.envs.hidenseek:MiniHackHideAndSeek",
)
