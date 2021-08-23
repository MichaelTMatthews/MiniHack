from nle.minihack import (
    MiniHackSkill,
    LevelGenerator,
    RewardManager,
)
from gym.envs import registration

from nle import nethack
from nle.minihack.envs.skill_transfer.interleaved_curriculum import MiniHackIC

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

MOVE_ACTIONS = tuple(nethack.CompassDirection)

WAND_LAVA_CROSS_COMMANDS = tuple(
    [
        *MOVE_ACTIONS,
        nethack.Command.PUTON,
        ord("z"),
        ord("f"),
        ord("g"),
        ord(","),
        ord("r"),
    ]
)


class MiniHackPickUpWand(MiniHackSkill):
    """PickUp a wand in a random location"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", WAND_LAVA_CROSS_COMMANDS)

        lvl_gen = LevelGenerator(w=10, h=10, lit=True)
        lvl_gen.add_object("cold", "/")
        # Add distractions to make skill more generalisable
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(WAND_NAMES)

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackZapColdWand(MiniHackSkill):
    """Zap a wand of cold and put out some lava"""

    def __init__(self, *args, **kwargs):
        # Enable autopickup, so we start with the wand in inventory
        kwargs["options"] = kwargs.pop("options", [])
        kwargs["options"].append("autopickup")
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", WAND_LAVA_CROSS_COMMANDS)

        des_file = "skill_transfer/cold_wand_zap.des"

        reward_manager = RewardManager()
        reward_manager.add_message_event(["The lava cools and solidifies."])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackNavigateLava(MiniHackSkill):
    """Navigate past random lava patches to the staircase"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", WAND_LAVA_CROSS_COMMANDS)

        super().__init__(*args, des_file="skill_transfer/navigate_lava.des", **kwargs)


class MiniHackLCWandPickup(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 400)
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", WAND_LAVA_CROSS_COMMANDS)

        super().__init__(
            *args, des_file="skill_transfer/lavacross_wand_pick.des", **kwargs
        )


class MiniHackLCWandPickupSkillsIC(MiniHackIC):
    """Environment that will either generate a robe or an apple."""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", WAND_LAVA_CROSS_COMMANDS)

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
                "skill_transfer/cold_wand_zap.des",
                "skill_transfer/navigate_lava.des",
            ],
            reward_managers=[
                reward_manager_pick,
                reward_manager_zap,
                reward_manager_navigate,
            ],
            **kwargs,
        )


registration.register(
    id="MiniHack-PickUpWand-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_lavacross:"
    "MiniHackPickUpWand",
)

registration.register(
    id="MiniHack-ZapColdWand-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_lavacross:"
    "MiniHackZapColdWand",
)

registration.register(
    id="MiniHack-LavaCross-Wand-PickUp-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_lavacross:"
    "MiniHackLCWandPickup",
)

registration.register(
    id="MiniHack-NavigateLava-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_lavacross:"
    "MiniHackNavigateLava",
)

registration.register(
    id="MiniHack-LavaCross-Wand-PickUp-IC-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_lavacross:"
    "MiniHackLCWandPickupSkillsIC",
)
