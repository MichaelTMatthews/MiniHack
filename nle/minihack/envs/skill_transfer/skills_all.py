from nle.minihack import (
    RewardManager,
)
from gym.envs import registration

from nle import nethack
from nle.minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer
from nle.minihack.envs.skill_transfer.task_simple import RING_NAMES
from nle.nethack import Command

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
        nethack.Command.WIELD,
        nethack.Command.QUAFF,  # Only for prep
        ord("$"),
        ord("f"),
        ord("g"),
        ord("h"),
    ]
)

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

AMULET_PREFIXES = [
    "circular",
    "spherical",
    "oval",
    "triangular",
    "pyramidal",
    "square",
    "concave",
    "hexagonal",
    "octagonal",
]


def a_or_an(adj):
    if adj == "uranium":  # ...
        return "a"
    if adj[0] in ["a", "e", "i", "o", "u"]:
        return "an"
    return "a"


WAND_NAMES = [("- " + a_or_an(pref) + " " + pref + " wand") for pref in WAND_PREFIXES]
AMULET_NAMES = [
    ("- " + a_or_an(pref) + " " + pref + " amulet") for pref in AMULET_PREFIXES
]


class MiniHackSkillApplyFrostHorn(MiniHackSkillTransfer):
    def __init__(self, *args, **kwargs):
        # Enable autopickup, so we start with the wand in inventory
        kwargs["options"] = kwargs.pop("options", [])
        kwargs["options"].append("autopickup")
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        des_file = "skill_transfer/skills/skill_apply_frost_horn.des"

        reward_manager = RewardManager()
        reward_manager.add_message_event(["The lava cools and solidifies."])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSkillEat(MiniHackSkillTransfer):
    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        des_file = "skill_transfer/skills/skill_eat.des"

        reward_manager = RewardManager()
        reward_manager.add_eat_event("apple")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSkillFight(MiniHackSkillTransfer):
    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        des_file = "skill_transfer/skills/skill_fight.des"

        reward_manager = RewardManager()
        reward_manager.add_message_event(
            ["You kill the wumpus!", "You hit the wumpus!", "You miss the wumpus."],
        )

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSkillNavigateBlind(MiniHackSkillTransfer):
    def __init__(self, *args, **kwargs):
        # Enable autopickup
        kwargs["options"] = kwargs.pop("options", [])
        kwargs["options"].append("autopickup")
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        des_file = "skill_transfer/skills/skill_navigate_blind.des"

        super().__init__(*args, des_file=des_file, **kwargs)

    def step(self, action: int):
        # Drink potion of blindness
        assert "inv_letters" in self._observation_keys

        inv_letters_index = self._observation_keys.index("inv_letters")

        inv_letters = self.last_observation[inv_letters_index]

        if ord("f") in inv_letters:
            self.env.step(Command.QUAFF)
            self.env.step(ord("f"))

        obs, reward, done, info = super().step(action)
        return obs, reward, done, info


class MiniHackSkillNavigateLava(MiniHackSkillTransfer):
    """Navigate past random lava patches to the staircase"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        super().__init__(
            *args, des_file="skill_transfer/skills/skill_navigate_lava.des", **kwargs
        )


class MiniHackSkillNavigateLavaToAmulet(MiniHackSkillTransfer):
    """Navigate past random lava patches to the staircase"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        reward_manager = RewardManager()
        reward_manager.add_message_event(
            ["amulet"],
        )

        super().__init__(
            *args,
            des_file="skill_transfer/skills/skill_navigate_lava_to_amulet.des",
            reward_manager=reward_manager,
            **kwargs,
        )


class MiniHackSkillNavigateOverLava(MiniHackSkillTransfer):
    """Navigate over random lava patches to the staircase"""

    def __init__(self, *args, **kwargs):
        # Enable autopickup
        kwargs["options"] = kwargs.pop("options", [])
        kwargs["options"].append("autopickup")
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        super().__init__(
            *args,
            des_file="skill_transfer/skills/skill_navigate_over_lava.des",
            **kwargs,
        )

    def step(self, action: int):
        # Drink potion of levitation
        assert "inv_letters" in self._observation_keys

        inv_letters_index = self._observation_keys.index("inv_letters")

        inv_letters = self.last_observation[inv_letters_index]

        if ord("f") in inv_letters:
            self.env.step(Command.QUAFF)
            self.env.step(ord("f"))

        obs, reward, done, info = super().step(action)
        return obs, reward, done, info


class MiniHackSkillNavigateWater(MiniHackSkillTransfer):
    """Navigate past random water patches to the staircase"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        reward_manager = RewardManager()
        reward_manager.add_message_event(["You try to crawl"], reward=-0.1)

        reward_manager.add_message_event(["You try dsadsato crawl"], reward=-0.1)

        super().__init__(
            *args,
            des_file="skill_transfer/skills/skill_navigate_water.des",
            reward_manager=reward_manager,
            **kwargs,
        )


class MiniHackSkillPickUp(MiniHackSkillTransfer):
    """PickUp Item"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        des_file = "skill_transfer/skills/skill_pick_up.des"

        reward_manager = RewardManager()
        reward_manager.add_message_event(
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


registration.register(
    id="MiniHack-Skill-ApplyFrostHorn-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:"
    "MiniHackSkillApplyFrostHorn",
)

registration.register(
    id="MiniHack-Skill-Eat-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:" "MiniHackSkillEat",
)

registration.register(
    id="MiniHack-Skill-Fight-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:" "MiniHackSkillFight",
)

registration.register(
    id="MiniHack-Skill-NavigateBlind-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:"
    "MiniHackSkillNavigateBlind",
)

registration.register(
    id="MiniHack-Skill-NavigateLava-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:"
    "MiniHackSkillNavigateLava",
)

registration.register(
    id="MiniHack-Skill-NavigateLavaToAmulet-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:"
    "MiniHackSkillNavigateLavaToAmulet",
)

registration.register(
    id="MiniHack-Skill-NavigateOverLava-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:"
    "MiniHackSkillNavigateOverLava",
)

registration.register(
    id="MiniHack-Skill-NavigateWater-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:"
    "MiniHackSkillNavigateWater",
)


registration.register(
    id="MiniHack-Skill-PickUp-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:" "MiniHackSkillPickUp",
)

registration.register(
    id="MiniHack-ZapColdWand-v1",
    entry_point="nle.minihack.envs.skill_transfer.skills_all:" "MiniHackZapColdWand",
)
