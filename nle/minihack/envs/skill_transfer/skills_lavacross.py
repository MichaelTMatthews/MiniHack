from nle.minihack import (
    MiniHackSkill,
    LevelGenerator,
    RewardManager,
)
from gym.envs import registration

from nle import nethack


RING_PREFIXES = [
    "pearl",
    "iron",
    "twisted",
    "steel",
    "wire",
    "engagement",
    "shiny",
    "bronze",
    "brass",
    "copper",
    "silver",
    "gold",
    "wooden",
    "granite",
    "opal",
    "clay",
    "coral",
    "black",
    "onyx",
    "moonstone",
    "tiger",
    "eye",
    "jade",
    "agate",
    "topaz",
    "sapphire",
    "ruby",
    "diamond",
    "ivory",
    "emerald",
]


def a_or_an(adj):
    if adj[0] in ["a", "e", "i", "o", "u"]:
        return "an"
    return "a"


RING_NAMES = [(a_or_an(pref) + " " + pref + " ring") for pref in RING_PREFIXES]

MOVE_ACTIONS = tuple(nethack.CompassDirection)

RING_LAVA_CROSS_COMMANDS = tuple(
    [*MOVE_ACTIONS, nethack.Command.PUTON, ord("r"), ord("l"), ord("f"), ord("g")]
)


class MiniHackPickUpLevitationRing(MiniHackSkill):
    """PickUp a ring in a random location"""

    def __init__(self, *args, **kwargs):
        kwargs["options"] = kwargs.pop("options", [])
        kwargs["options"].append("autopickup")

        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", RING_LAVA_CROSS_COMMANDS)

        lvl_gen = LevelGenerator(w=10, h=10, lit=True)
        lvl_gen.add_object("levitation", "=")
        # Add distractions to make skill more generalisable
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(RING_PREFIXES)

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPutOnLevitationRing(MiniHackSkill):
    """PutOn a ring in a random location"""

    def __init__(self, *args, **kwargs):
        kwargs["options"] = kwargs.pop("options", [])
        kwargs["options"].append("autopickup")

        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", RING_LAVA_CROSS_COMMANDS)

        lvl_gen = LevelGenerator(w=10, h=10, lit=True)
        lvl_gen.add_object("levitation", "=")
        # Add distractions to make skill more generalisable
        # lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(
            [
                "a ring of levitation (on right hand)",
                "a ring of levitation (on left hand)",
            ]
        )

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackLCLevitateRingPickupComposed(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 400)
        # kwargs["options"] = kwargs.pop("options", [])
        # kwargs["options"].append("autopickup")
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", RING_LAVA_CROSS_COMMANDS)
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
OBJECT:('=',"levitation"),rndcoord($left_bank),blessed
BRANCH:(1,1,5,5),(0,0,0,0)
STAIR:rndcoord($right_bank),down
"""
        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-PickUpLevitationRing-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_lavacross:"
    "MiniHackPickUpLevitationRing",
)

registration.register(
    id="MiniHack-PutOnLevitationRing-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_lavacross:"
    "MiniHackPutOnLevitationRing",
)

registration.register(
    id="MiniHack-LavaCross-Ring-PickUp-Composed-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_lavacross:"
    "MiniHackLCLevitateRingPickupComposed",
)
