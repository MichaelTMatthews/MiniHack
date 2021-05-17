from nle.minihack import MiniHackSkill, LevelGenerator, RewardManager
from gym.envs import registration

freeze_msgs = [
    "The bolt of cold bounces!",  # checks if cold bounces from the wall
]


class MiniHackFreeze(MiniHackSkill):
    def __init__(self, *args, des_file, **kwargs):
        rwrd_mngr = RewardManager()
        rwrd_mngr.add_message_event(freeze_msgs)

        super().__init__(*args, des_file=des_file, reward_manager=rwrd_mngr, **kwargs)


class MiniHackFreezeWand(MiniHackFreeze):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=8, h=8, lit=True)
        lvl_gen.add_object("cold", "/", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackFreezeHorn(MiniHackFreeze):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=8, h=8, lit=True)
        lvl_gen.add_object("frost horn", "(", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackFreezeRandom(MiniHackFreeze):
    def __init__(self, *args, n_distract=0, **kwargs):
        des_file = """
MAZE: "mylevel", ' '
FLAGS:hardfloor
MESSAGE: "Welcome to MiniHack!"
INIT_MAP: solidfill,' '
GEOMETRY:center,center
MAP
.....
.....
.....
.....
.....
ENDMAP
REGION:(0,0,8,8),lit,"ordinary"
IF [50%] {
    OBJECT:('/',"cold"),random,blessed
} ELSE {
    OBJECT:('(',"frost horn"),random,blessed
}
"""
        for _ in range(n_distract):
            des_file += "OBJECT:random,random\n"
        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackFreezeRandomDist(MiniHackFreezeRandom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, n_distract=3, **kwargs)


registration.register(
    id="MiniHack-Freeze-Wand-v0",
    entry_point="nle.minihack.envs.skills_freeze:MiniHackFreezeWand",
)
registration.register(
    id="MiniHack-Freeze-Horn-v0",
    entry_point="nle.minihack.envs.skills_freeze:MiniHackFreezeHorn",
)
registration.register(
    id="MiniHack-Freeze-Random-v0",
    entry_point="nle.minihack.envs.skills_freeze:MiniHackFreezeRandom",
)
registration.register(
    id="MiniHack-Freeze-Random-Distract-v0",
    entry_point="nle.minihack.envs.skills_freeze:MiniHackFreezeRandomDist",
)
