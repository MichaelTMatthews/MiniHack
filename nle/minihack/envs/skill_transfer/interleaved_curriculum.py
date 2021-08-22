from nle.minihack import MiniHackSkill
import numpy as np


class MiniHackIC(MiniHackSkill):
    """The base class for interleaved curriculum.  Pass it a list of des files
    and on each environment reset a random one will be selected."""

    def __init__(self, *args, des_files, reward_manager, **kwargs):
        self.des_files = des_files

        super().__init__(
            *args, des_file=self.sample_des(), reward_manager=reward_manager, **kwargs
        )

    def sample_des(self):
        return np.random.choice(self.des_files)

    def reset(self, *args, **kwargs):
        self.update(self.sample_des())
        return super().reset(*args, **kwargs)
