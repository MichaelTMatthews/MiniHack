from nle.minihack import MiniHackSkill, LevelGenerator, RewardManager
from gym.envs import registration


class MiniHackEat(MiniHackSkill):
    """Environment for "eat" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("apple", "%")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_eat_event("apple")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackWield(MiniHackSkill):
    """Environment for "wield" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("dagger", ")")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wield_event("dagger")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackWear(MiniHackSkill):
    """Environment for "wear" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("robe", "[")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wear_event("robe")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPutOn(MiniHackSkill):
    """Environment for "put on" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("amulet of life saving", '"')
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_amulet_event()

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackZap(MiniHackSkill):
    """Environment for "zap" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("enlightenment", "/")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(["The feeling subsides."])  # TODO change

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackRead(MiniHackSkill):
    """Environment for "read" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("blank paper", "?")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(
            ["This scroll seems to be blank."]
        )  # TODO change

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPray(MiniHackSkill):
    """Environment for "pray" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_altar("random", "neutral", "altar")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_positional_event("altar", "pray")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSink(MiniHackSkill):
    """Environment for "sink" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_sink()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_positional_event("sink", "quaff")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackClosedDoor(MiniHackSkill):
    """Environment for "open" task."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="closed_door.des", **kwargs)


class MiniHackLockedDoor(MiniHackSkill):
    """Environment for "kick" task."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="locked_door.des", **kwargs)


# Skill Tasks
registration.register(
    id="MiniHack-Eat-v0",
    entry_point="nle.minihack.envs.skills_simple:MiniHackEat",
)
registration.register(
    id="MiniHack-Pray-v0",
    entry_point="nle.minihack.envs.skills_simple:MiniHackPray",
)
registration.register(
    id="MiniHack-Sink-v0",
    entry_point="nle.minihack.envs.skills_simple:MiniHackSink",
)
registration.register(
    id="MiniHack-ClosedDoor-v0",
    entry_point="nle.minihack.envs.skills_simple:MiniHackClosedDoor",
)
registration.register(
    id="MiniHack-LockedDoor-v0",
    entry_point="nle.minihack.envs.skills_simple:MiniHackLockedDoor",
)
registration.register(
    id="MiniHack-Wield-v0",
    entry_point="nle.minihack.envs.skills_simple:MiniHackWield",
)
registration.register(
    id="MiniHack-Wear-v0",
    entry_point="nle.minihack.envs.skills_simple:MiniHackWear",
)
registration.register(
    id="MiniHack-PutOn-v0",
    entry_point="nle.minihack.envs.skills_simple:MiniHackPutOn",
)
registration.register(
    id="MiniHack-Zap-v0",
    entry_point="nle.minihack.envs.skills_simple:MiniHackZap",
)
registration.register(
    id="MiniHack-Read-v0",
    entry_point="nle.minihack.envs.skills_simple:MiniHackRead",
)
