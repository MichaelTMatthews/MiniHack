from nle.minihack import LevelGenerator, RewardManager
from gym.envs import registration

from nle.minihack.envs.skill_transfer import skills_all
from nle.minihack.envs.skill_transfer.interleaved_curriculum import MiniHackIC
from nle.minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer

WAND_PREFIXES = [
    "glass",
    "balsa",
    "crystal",
    "maple",
    "pine",
    "oak",
    "ebony",
    "marble",
    "tin",
    "brass",
    "copper",
    "silver",
    "platinum",
    "iridium",
    "zinc",
    "aluminum",
    "uranium",
    "iron",
    "steel",
    "hexagonal",
    "short",
    "runed",
    "long",
    "curved",
    "forked",
    "spiked",
    "jeweled",
]


def a_or_an(adj):
    if adj == "uranium":  # ...
        return "a"
    if adj[0] in ["a", "e", "i", "o", "u"]:
        return "an"
    return "a"


WAND_NAMES = [("- " + a_or_an(pref) + " " + pref + " wand") for pref in WAND_PREFIXES]


class MiniHackLCFreeze(MiniHackSkillTransfer):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 400)
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        super().__init__(
            *args,
            des_file="skill_transfer/tasks/task_lavacross_freeze.des",
            **kwargs,
        )


class MiniHackLCWandPickupSkillsIC(MiniHackIC):
    """Environment that will either generate a robe or an apple."""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        lvl_gen = LevelGenerator(w=10, h=10, lit=True)
        lvl_gen.add_object("cold", "/")
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file_pick = lvl_gen.get_des()

        reward_manager_pick = RewardManager()
        reward_manager_pick.add_message_event(WAND_NAMES)

        reward_manager_zap = RewardManager()
        reward_manager_zap.add_message_event(["The lava cools and solidifies."])

        reward_manager_navigate = None

        super().__init__(
            *args,
            des_files=[
                des_file_pick,
                "skill_transfer/skills/skill_zap_cold.des",
                "skill_transfer/skills/skill_navigate_lava.des",
            ],
            reward_managers=[
                reward_manager_pick,
                reward_manager_zap,
                reward_manager_navigate,
            ],
            **kwargs,
        )


registration.register(
    id="MiniHack-LavaCrossFreeze-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_lavacross:" "MiniHackLCFreeze",
)

registration.register(
    id="MiniHack-LavaCross-Wand-PickUp-IC-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_lavacross:"
    "MiniHackLCWandPickupSkillsIC",
)
