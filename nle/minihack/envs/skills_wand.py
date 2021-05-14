from nle.minihack import MiniHackSkill, LevelGenerator, RewardManager
from gym.envs import registration


class MiniHackWoDEasy(MiniHackSkill):
    """Environment for "Wand of death" task."""

    def __init__(self, *args, **kwargs):
        map = """
|----------
|.........+
|----------
"""
        lvl_gen = LevelGenerator(map=map, lit=True)

        lvl_gen.set_start_pos((1, 1))
        kwargs["options"] = kwargs.pop("options", [])
        kwargs["options"].append("autopickup")

        lvl_gen.add_object(
            name="death", symbol="/", cursestate="blessed", place=((1, 1))
        )
        lvl_gen.add_monster("minotaur", args=("asleep",), place=(9, 1))

        des_file = lvl_gen.get_des()

        rwrd_mngr = RewardManager()
        rwrd_mngr.add_kill_event("minotaur")

        super().__init__(*args, des_file=des_file, reward_manager=rwrd_mngr, **kwargs)


class MiniHackWoDMedium(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        map = """
|---------------------------|
|...........................|
|---------------------------|
"""
        lvl_gen = LevelGenerator(map=map, lit=True)

        lvl_gen.set_start_pos((1, 1))
        lvl_gen.add_goal_pos((27, 1))

        lvl_gen.add_object(
            name="death", symbol="/", cursestate="blessed", place=((2, 1))
        )
        lvl_gen.add_monster("minotaur", args=("asleep",), place=(26, 1))

        des_file = lvl_gen.get_des()
        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackWoDHard(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        map = """
-------
|.....|
|.....|---------------------|
|...........................|
|.....|---------------------|
|.....|
|-----|
"""
        lvl_gen = LevelGenerator(map=map, lit=True)

        lvl_gen.set_start_rect((1, 1), (5, 5))
        lvl_gen.add_goal_pos((27, 3))

        lvl_gen.set_area_variable("$safe_room", "fillrect", 1, 1, 5, 5)
        lvl_gen.add_object_area(
            "$safe_room", name="death", symbol="/", cursestate="blessed"
        )
        lvl_gen.add_monster("minotaur", place=(26, 3))
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackWoDExtreme(MiniHackSkill):
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
    id="MiniHack-WoD-Easy-v0",
    entry_point="nle.minihack.envs.skills_wand:MiniHackWoDEasy",
)

registration.register(
    id="MiniHack-WoD-Medium-v0",
    entry_point="nle.minihack.envs.skills_wand:MiniHackWoDMedium",
)
registration.register(
    id="MiniHack-WoD-Hard-v0",
    entry_point="nle.minihack.envs.skills_wand:MiniHackWoDHard",
)
registration.register(
    id="MiniHack-WoD-Extreme-v0",
    entry_point="nle.minihack.envs.skills_wand:MiniHackWoDExtreme",
)
