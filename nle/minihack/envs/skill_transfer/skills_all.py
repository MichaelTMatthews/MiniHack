from nle.minihack import (
    LevelGenerator,
    RewardManager,
)
from gym.envs import registration

from nle import nethack
from nle.minihack.envs.skill_transfer import task_lavacross
from nle.minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer


MOVE_ACTIONS = tuple(nethack.CompassDirection)

COMMANDS = tuple(
    [
        *MOVE_ACTIONS,
        nethack.Command.PICKUP,
        nethack.Command.PUTON,
        nethack.Command.ZAP,
        nethack.Command.TAKEOFF,
        nethack.Command.WEAR,
        nethack.Command.THROW,
        nethack.Command.ESC,
        nethack.Command.EAT,
        nethack.Command.APPLY,
        ord("$"),
        ord("f"),
        ord("g"),
        ord("h"),
    ]
)


class MiniHackPickUpWand(MiniHackSkillTransfer):
    """PickUp a wand in a random location"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        lvl_gen = LevelGenerator(w=10, h=10, lit=True)
        lvl_gen.add_object("cold", "/")
        # Add distractions to make skill more generalisable
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(task_lavacross.WAND_NAMES)

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackZapColdWand(MiniHackSkillTransfer):
    """Zap a wand of cold and put out some lava"""

    def __init__(self, *args, **kwargs):
        # Enable autopickup, so we start with the wand in inventory
        kwargs["options"] = kwargs.pop("options", [])
        kwargs["options"].append("autopickup")
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        des_file = "skill_transfer/skills/skill_zap_cold.des"

        reward_manager = RewardManager()
        reward_manager.add_message_event(["The lava cools and solidifies."])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackNavigateLava(MiniHackSkillTransfer):
    """Navigate past random lava patches to the staircase"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        super().__init__(
            *args, des_file="skill_transfer/skills/skill_navigate_lava.des", **kwargs
        )


registration.register(
    id="MiniHack-PickUpWand-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:" "MiniHackPickUpWand",
)

registration.register(
    id="MiniHack-ZapColdWand-v1",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:" "MiniHackZapColdWand",
)

registration.register(
    id="MiniHack-NavigateLava-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:" "MiniHackNavigateLava",
)
