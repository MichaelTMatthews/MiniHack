from nle.minihack import MiniHackSkill, LevelGenerator, RewardManager
from gym.envs import registration


levitation_msg = [
    "You float up",
    "You start to float in the air",
    "Up, up, and awaaaay!",
    "a ring of levitation (on left hand)",
    "a ring of levitation (on right hand)",
]


class MiniHackLevitate(MiniHackSkill):
    def __init__(self, *args, des_file, **kwargs):
        rwrd_mngr = RewardManager()
        rwrd_mngr.add_message_event(levitation_msg)

        super().__init__(*args, des_file=des_file, reward_manager=rwrd_mngr, **kwargs)


class MiniHackLevitateBoots(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("levitation boots", "[", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackLevitateRing(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("levitation", "=", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackLevitatePotion(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("levitation", "!", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackLevitateRandom(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        des_file = """
MAZE: "mylevel", ' '
FLAGS:hardfloor
INIT_MAP: solidfill,' '
GEOMETRY:center,center
MAP
.....
.....
.....
.....
.....
ENDMAP
REGION:(0,0,5,5),lit,"ordinary"
IF [33%] {
    OBJECT:('!',"levitation"),random,blessed
} ELSE {
    IF [50%] {
        OBJECT:('=',"levitation"),random,blessed
    } ELSE {
        OBJECT:('[',"levitation boots"),random,blessed
    }
}
"""
        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackLevitateLava(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        des_file = """
MAZE: "mylevel", ' '
FLAGS:hardfloor
INIT_MAP: solidfill,' '
GEOMETRY:center,center
MAP
-------------
|.....L.....|
|.....L.....|
|.....L.....|
|.....L.....|
|.....L.....|
-------------
ENDMAP
REGION:(0,0,12,6),lit,"ordinary"
$left_bank = selection:fillrect (1,1,5,5)
$right_bank = selection:fillrect (7,1,11,5)
IF [33%] {
    OBJECT:('!',"levitation"),rndcoord($left_bank),blessed
} ELSE {
    IF [50%] {
        OBJECT:('=',"levitation"),rndcoord($left_bank),blessed
    } ELSE {
        OBJECT:('[',"levitation boots"),rndcoord($left_bank),blessed
    }
}
BRANCH:(1,1,5,5),(0,0,0,0)
STAIR:rndcoord($right_bank),down
"""
        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-Levitate-Boots-v0",
    entry_point="nle.minihack.envs.skills_levitate:MiniHackLevitateBoots",
)
registration.register(
    id="MiniHack-Levitate-Ring-v0",
    entry_point="nle.minihack.envs.skills_levitate:MiniHackLevitateRing",
)
registration.register(
    id="MiniHack-Levitate-Potion-v0",
    entry_point="nle.minihack.envs.skills_levitate:MiniHackLevitatePotion",
)
registration.register(
    id="MiniHack-Levitate-Random-v0",
    entry_point="nle.minihack.envs.skills_levitate:MiniHackLevitateRandom",
)
registration.register(
    id="MiniHack-Levitate-Lava-v0",
    entry_point="nle.minihack.envs.skills_levitate:MiniHackLevitateLava",
)
