# Copyright (c) Facebook, Inc. and its affiliates.
from nle.minihack import MiniHack, LevelGenerator, RewardManager
from nle.nethack import CompassDirection
from gym.envs import registration
import numpy as np

Y_cmd = CompassDirection.NW


class MiniHackSkillEnv(MiniHack):
    """Base environment skill acquisition tasks."""

    def __init__(
        self,
        *args,
        des_file,
        reward_manager=None,
        **kwargs,
    ):
        """If reward_manager == None, the goal is to reach the staircase."""
        kwargs["options"] = kwargs.pop("options", [])
        kwargs["options"].append("pettype:none")
        kwargs["options"].append("!autopickup")
        kwargs["character"] = kwargs.pop("charachter", "cav-hum-new-mal")
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 100)
        self._no_rand_mon()

        default_keys = [
            "chars_crop",
            "colors_crop",
            "screen_descriptions_crop",
            "message",
            "inv_strs",
            "inv_letters",
        ]

        kwargs["observation_keys"] = kwargs.pop("observation_keys", default_keys)
        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackEat(MiniHackSkillEnv):
    """Environment for "eat" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("apple", "%")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_eat_event("apple")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackWield(MiniHackSkillEnv):
    """Environment for "wield" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("dagger", ")")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wield_event("dagger")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackWear(MiniHackSkillEnv):
    """Environment for "wear" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("robe", "[")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wear_event("robe")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackTakeOff(MiniHackSkillEnv):
    """Environment for "take off" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("leather jacket", "[")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wear_event("leather jacket")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPutOn(MiniHackSkillEnv):
    """Environment for "put on" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("amulet of life saving", '"')
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_amulet_event()

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackZap(MiniHackSkillEnv):
    """Environment for "zap" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("enlightenment", "/")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(["The feeling subsides."])  # TODO change

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackRead(MiniHackSkillEnv):
    """Environment for "read" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("blank paper", "?")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(
            ["This scroll seems to be blank."]
        )  # TODO change

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPray(MiniHackSkillEnv):
    """Environment for "pray" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_altar("random", "neutral", "altar")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_positional_event("altar", "pray")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSink(MiniHackSkillEnv):
    """Environment for "sink" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_sink()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_positional_event("sink", "quaff")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackClosedDoor(MiniHackSkillEnv):
    """Environment for "open" task."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="closed_door.des", **kwargs)


class MiniHackLockedDoor(MiniHackSkillEnv):
    """Environment for "kick" task."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="locked_door.des", **kwargs)


class MiniHackWandOfDeath(MiniHackSkillEnv):
    """Environment for "Wand of death" task."""

    def __init__(self, *args, **kwargs):
        map = """
-------------
|...........|
|...........|
|...........|
|...........|
|....|.|....|
|....|.|....|
|-----.-----|
|...........|
|...........|
|...........|
-------------
"""
        lvl_gen = LevelGenerator(map=map, lit=True)

        def get_safe_coord():
            return np.random.randint(1, 11), np.random.randint(1, 5)

        def get_dangerous_coord():
            return np.random.randint(1, 11), np.random.randint(8, 10)

        lvl_gen.add_object("death", "/", cursestate="blessed", place=get_safe_coord())
        lvl_gen.add_stair_up(get_safe_coord())
        lvl_gen.add_monster("minotaur", args=("asleep",), place=(6, 8))
        lvl_gen.add_stair_down(get_dangerous_coord())
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-WandOfDeath-v0",
    entry_point="nle.minihack.skills:MiniHackWandOfDeath",
)


class MiniHackLabyrinth(MiniHackSkillEnv):
    """Environment for "Labyrinth" task."""

    def __init__(self, *args, **kwargs):
        map = """
-------------------------------------
|.................|.|...............|
|.|-------------|.|.|.------------|.|
|.|.............|.|.|.............|.|
|.|.|----------.|.|.|------------.|.|
|.|.|...........|.|.............|.|.|
|.|.|.|----------.|-----------|.|.|.|
|.|.|.|...........|.......|...|.|.|.|
|.|.|.|.|----------------.|.|.|.|.|.|
|.|.|.|.|.................|.|.|.|.|.|
|.|.|.|.|.-----------------.|.|.|.|.|
|.|.|.|.|...................|.|.|.|.|
|.|.|.|.|--------------------.|.|.|.|
|.|.|.|.......................|.|.|.|
|.|.|.|-----------------------|.|.|.|
|.|.|...........................|.|.|
|.|.|---------------------------|.|.|
|.|...............................|.|
|.|-------------------------------|.|
|...................................|
-------------------------------------
"""
        lvl_gen = LevelGenerator(map=map, lit=True)
        lvl_gen.add_stair_up((19, 1))
        lvl_gen.add_stair_down((19, 7))
        lvl_gen.add_monster(name="minotaur", place=(19, 9))
        lvl_gen.add_object("death", "/", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(
            *args,
            des_file=des_file,
            **kwargs,
        )


registration.register(
    id="MiniHack-Labyrinth-v0",
    entry_point="nle.minihack.skills:MiniHackLabyrinth",
)


# Skill Tasks
registration.register(
    id="MiniHack-Eat-v0",
    entry_point="nle.minihack.skills:MiniHackEat",
)
registration.register(
    id="MiniHack-Pray-v0",
    entry_point="nle.minihack.skills:MiniHackPray",
)
registration.register(
    id="MiniHack-Sink-v0",
    entry_point="nle.minihack.skills:MiniHackSink",
)
registration.register(
    id="MiniHack-ClosedDoor-v0",
    entry_point="nle.minihack.skills:MiniHackClosedDoor",
)
registration.register(
    id="MiniHack-LockedDoor-v0",
    entry_point="nle.minihack.skills:MiniHackLockedDoor",
)
registration.register(
    id="MiniHack-Wield-v0",
    entry_point="nle.minihack.skills:MiniHackWield",
)
registration.register(
    id="MiniHack-Wear-v0",
    entry_point="nle.minihack.skills:MiniHackWear",
)
registration.register(
    id="MiniHack-TakeOff-v0",
    entry_point="nle.minihack.skills:MiniHackTakeOff",
)
registration.register(
    id="MiniHack-PutOn-v0",
    entry_point="nle.minihack.skills:MiniHackPutOn",
)
registration.register(
    id="MiniHack-Zap-v0",
    entry_point="nle.minihack.skills:MiniHackZap",
)
registration.register(
    id="MiniHack-Read-v0",
    entry_point="nle.minihack.skills:MiniHackRead",
)
