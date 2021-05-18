from nle.minihack import MiniHackSkill
from gym.envs import registration


class MiniHackLavaCross(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="lava_crossing.des", **kwargs)


registration.register(
    id="MiniHack-LavaCross-v0",
    entry_point="nle.minihack.envs.skills_lava:MiniHackLavaCross",
)
