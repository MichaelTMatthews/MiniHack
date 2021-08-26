from nle.minihack import MiniHackSkill
from gym.envs import registration

from nle import nethack

MOVE_ACTIONS = tuple(nethack.CompassDirection)

COMMANDS = tuple(
    [
        *MOVE_ACTIONS,
        ord(","),
        ord("f"),
        nethack.Command.WEAR,
        nethack.Command.APPLY,
        ord("g"),
    ]
)


class MiniHackSeaMonsters(MiniHackSkill):
    """PickUp a wand in a random location"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        des_file = "skill_transfer/sea_monsters.des"

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackWeaponSwitch(MiniHackSkill):
    """PickUp a wand in a random location"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", COMMANDS)

        des_file = "skill_transfer/weapon_switch.des"

        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-SeaMonsters-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_scrap:" "MiniHackSeaMonsters",
)

registration.register(
    id="MiniHack-WeaponSwitch-v0",
    entry_point="nle.minihack.envs.skill_transfer.skills_scrap:" "MiniHackWeaponSwitch",
)
