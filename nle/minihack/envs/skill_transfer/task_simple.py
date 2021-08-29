from gym.envs import registration

from nle.minihack import RewardManager, IntersectionRewardManager
from nle.minihack.envs.skill_transfer import skills_all
from nle.minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer


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
    "black onyx",
    "moonstone",
    "tiger eye",
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


RING_NAMES = [("- " + a_or_an(pref) + " " + pref + " ring") for pref in RING_PREFIXES]


class MiniHackSimpleSeq(MiniHackSkillTransfer):
    """Simple Sequence of skills"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_file = "skill_transfer/tasks/task_simple_seq.des"

        reward_manager = RewardManager()
        reward_manager.add_message_event(
            ["You kill the wumpus!"],
        )

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSimpleIntersection(MiniHackSkillTransfer):
    """Simple Intersection of skills"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_file = "skill_transfer/tasks/task_simple_intersection.des"

        reward_manager = IntersectionRewardManager()
        reward_manager.add_eat_event("apple", reward=0.5)
        reward_manager.add_wear_event("leather cloak", reward=0.5)

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSimpleRandom(MiniHackSkillTransfer):
    """Simple Randomised sequence of skills"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_file = "skill_transfer/tasks/task_simple_random.des"

        reward_manager = RewardManager()
        reward_manager.add_message_event(["You kill the orc!"])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSimpleUnion(MiniHackSkillTransfer):
    """Simple Union of skills"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_file = "skill_transfer/tasks/task_simple_union.des"

        reward_manager = RewardManager()
        reward_manager.add_message_event(["You kill the orc!"])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


registration.register(
    id="MiniHack-SimpleSeq-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:" "MiniHackSimpleSeq",
)

registration.register(
    id="MiniHack-SimpleIntersection-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:"
    "MiniHackSimpleIntersection",
)

registration.register(
    id="MiniHack-SimpleRandom-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:" "MiniHackSimpleRandom",
)

registration.register(
    id="MiniHack-SimpleUnion-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:" "MiniHackSimpleUnion",
)
