from nle.minihack import (
    MiniHackSkill,
    LevelGenerator,
    IntersectionRewardManager,
    RewardManager,
)
from gym.envs import registration
import numpy as np

# python -m nle.scripts.play --env MiniHack-EatAndWear-Fixed-v0


class MiniHackEatAndWearFixed(MiniHackSkill):
    """Environment that is completed by performing both 'Eat' and 'Wear' skills"""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)

        lvl_gen.add_object("robe", "[", place=(4, 0))
        lvl_gen.add_object("apple", "%", place=(0, 0))

        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        reward_manager = IntersectionRewardManager()
        reward_manager.add_eat_event("apple")
        reward_manager.add_wear_event("robe")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackEatOrWearFixed(MiniHackSkill):
    """Environment that will either generate a robe or an apple."""

    def __init__(self, *args, **kwargs):
        reward_manager = RewardManager()
        reward_manager.add_eat_event("apple", terminal_sufficient=True)
        reward_manager.add_wear_event("robe", terminal_sufficient=True)

        super().__init__(
            *args, des_file="eat_or_wear.des", reward_manager=reward_manager, **kwargs
        )


class MiniHackEatOrWearFixed2(MiniHackSkill):
    """Environment that will either generate a robe or an apple."""

    def __init__(self, *args, **kwargs):
        reward_manager = RewardManager()
        reward_manager.add_eat_event("apple", terminal_sufficient=True)
        reward_manager.add_wear_event("robe", terminal_sufficient=True)

        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("apple", "%", place=(0, 0))
        lvl_gen.set_start_pos((2, 2))
        self.eat_des = lvl_gen.get_des()

        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("robe", "[", place=(4, 0))
        lvl_gen.set_start_pos((2, 2))
        self.wear_des = lvl_gen.get_des()

        super().__init__(
            *args, des_file=self.eat_des, reward_manager=reward_manager, **kwargs
        )

        self.reset()

    def reset(self, *args, **kwargs):
        des = self.eat_des
        if np.random.random() < 0.5:
            des = self.wear_des
        self.update(des)
        return super().reset(*args, **kwargs)


class MiniHackEatAndPray(MiniHackSkill):
    """Environment that is completed by performing both 'Eat' and 'Pray' skills"""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)

        lvl_gen.add_object("apple", "%")
        lvl_gen.add_altar("random", "neutral", "altar")

        des_file = lvl_gen.get_des()

        reward_manager = IntersectionRewardManager()
        reward_manager.add_eat_event("apple")
        reward_manager.add_positional_event("altar", "pray")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPickUp(MiniHackSkill):
    """PickUp one of the lava cross items"""

    def __init__(self, *args, **kwargs):
        kwargs["options"] = kwargs.pop("options", [])
        kwargs["options"].append("autopickup")

        self.df1 = """
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
$right_bank = selection:fillrect (7,1,11,5)
OBJECT:('!',"levitation"),(2,2),blessed
BRANCH:(2,2,2,2),(0,0,0,0)
STAIR:rndcoord($right_bank),down
"""

        df2 = """
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

        reward_manager = RewardManager()
        reward_manager.add_eat_event("apple")

        super().__init__(
            *args, des_file=self.df1, reward_manager=reward_manager, **kwargs
        )

        self.update(df2)
        print("update")

    def reset(self, *args, **kwargs):
        self.update(self.df1)
        print("RELOAD")
        return super().reset(*args, **kwargs)


registration.register(
    id="MiniHack-EatAndWear-Fixed-v0",
    entry_point="nle.minihack.envs.skills_composed:MiniHackEatAndWearFixed",
)

registration.register(
    id="MiniHack-EatOrWear-Fixed-v0",
    entry_point="nle.minihack.envs.skills_composed:MiniHackEatOrWearFixed",
)

registration.register(
    id="MiniHack-EatOrWear-Fixed2-v0",
    entry_point="nle.minihack.envs.skills_composed:MiniHackEatOrWearFixed2",
)

registration.register(
    id="MiniHack-EatAndPray-v0",
    entry_point="nle.minihack.envs.skills_composed:MiniHackEatAndPray",
)

registration.register(
    id="MiniHack-PickUp-v0",
    entry_point="nle.minihack.envs.skills_composed:MiniHackPickUp",
)
