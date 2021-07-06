from nle.minihack import (
    MiniHackSkill,
    LevelGenerator,
    IntersectionRewardManager,
    RewardManager,
)
from gym.envs import registration

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


registration.register(
    id="MiniHack-EatAndWear-Fixed-v0",
    entry_point="nle.minihack.envs.skills_composed:MiniHackEatAndWearFixed",
)

registration.register(
    id="MiniHack-EatOrWear-Fixed-v0",
    entry_point="nle.minihack.envs.skills_composed:MiniHackEatOrWearFixed",
)
