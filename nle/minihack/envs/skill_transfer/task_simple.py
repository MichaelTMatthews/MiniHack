from gym.envs import registration

from nle.minihack.envs.skill_transfer import skills_all
from nle.minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer


class MiniHackSimpleSeq(MiniHackSkillTransfer):
    """PickUp a wand in a random location"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_file = "skill_transfer/tasks/task_simple_seq.des"

        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-SimpleSeq-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_simple:" "MiniHackSimpleSeq",
)
