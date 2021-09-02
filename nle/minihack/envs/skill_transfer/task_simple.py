from gym.envs import registration

from nle.minihack import RewardManager, IntersectionRewardManager
from nle.minihack.envs.skill_transfer import skills_all
from nle.minihack.envs.skill_transfer.interleaved_curriculum import MiniHackIC
from nle.minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer
from nle.minihack.envs.skill_transfer.skills_all import (
    WAND_NAMES,
    AMULET_NAMES,
    RING_NAMES,
)


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


class MiniHackSimpleSeqIC(MiniHackIC):
    """Simple Sequence of skills interleaved curriculum"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_files = [
            "skill_transfer/skills/skill_pick_up.des",
            "skill_transfer/skills/skill_wield.des",
            "skill_transfer/skills/skill_fight.des",
        ]

        reward_manager_pu = RewardManager()
        reward_manager_pu.add_message_event(
            [
                "f - a silver saber",
                "f - a leather cloak",
                *RING_NAMES,
                "f - a key",
                *WAND_NAMES,
                "f - a dagger",
                "f - a horn",
                "f - a towel",
                "f - a green dragon scale mail",
                "$ - a gold piece",
                *AMULET_NAMES,
            ]
        )

        reward_manager_w = RewardManager()
        reward_manager_w.add_message_event(["a silver saber (weapon in hand)"])

        reward_manager_f = RewardManager()
        reward_manager_f.add_message_event(
            ["You kill the wumpus!", "You hit the wumpus!", "You miss the wumpus."],
        )

        reward_managers = [reward_manager_pu, reward_manager_w, reward_manager_f]

        super().__init__(
            *args, des_files=des_files, reward_managers=reward_managers, **kwargs
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


class MiniHackSimpleIntersectionIC(MiniHackIC):
    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_files = [
            "skill_transfer/skills/skill_pick_up.des",
            "skill_transfer/skills/skill_eat.des",
            "skill_transfer/skills/skill_wear.des",
        ]

        reward_manager_pu = RewardManager()
        reward_manager_pu.add_message_event(
            [
                "f - a silver saber",
                "f - a leather cloak",
                *RING_NAMES,
                "f - a key",
                *WAND_NAMES,
                "f - a dagger",
                "f - a horn",
                "f - a towel",
                "f - a green dragon scale mail",
                "$ - a gold piece",
                *AMULET_NAMES,
            ]
        )

        reward_manager_e = RewardManager()
        reward_manager_e.add_eat_event("apple")

        reward_manager_w = RewardManager()
        reward_manager_w.add_message_event(["You are now wearing a robe"])

        reward_managers = [reward_manager_pu, reward_manager_e, reward_manager_w]

        super().__init__(
            *args, des_files=des_files, reward_managers=reward_managers, **kwargs
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

        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-SimpleSeq-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:" "MiniHackSimpleSeq",
)

registration.register(
    id="MiniHack-SimpleSeq-IC-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:" "MiniHackSimpleSeqIC",
)

registration.register(
    id="MiniHack-SimpleIntersection-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:"
    "MiniHackSimpleIntersection",
)

registration.register(
    id="MiniHack-SimpleIntersectionIC-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:"
    "MiniHackSimpleIntersectionIC",
)

registration.register(
    id="MiniHack-SimpleRandom-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:" "MiniHackSimpleRandom",
)

registration.register(
    id="MiniHack-SimpleUnion-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:" "MiniHackSimpleUnion",
)
