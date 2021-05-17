from gym.envs import registration
from nle.minihack import MiniHackNavigation, RewardManager


class MiniHackMemento(MiniHackNavigation):
    """Environment for a memento challenge."""

    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 5000)
        reward_manager = RewardManager()
        reward_manager.add_message_event(
            ["squeak"], reward=-1, terminal_sufficient=True, terminal_required=True
        )
        reward_manager.add_kill_event(
            "grid bug", reward=1, terminal_sufficient=True, terminal_required=True
        )
        super().__init__(
            *args, des_file="memento.des", reward_manager=reward_manager, **kwargs
        )


registration.register(
    id="MiniHack-Memento-v0",
    entry_point="nle.minihack.envs.memento:MiniHackMemento",
)
