from nle.minihack import MiniHackSkill
from gym.envs import registration


class MiniHackQuest(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 1000)
        super().__init__(*args, des_file="quest.des", **kwargs)


class MiniHackQuestPro(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 1000)
        super().__init__(*args, des_file="quest_pro.des", **kwargs)


registration.register(
    id="MiniHack-Quest-v0",
    entry_point="nle.minihack.envs.skills_quest:MiniHackQuest",
)
registration.register(
    id="MiniHack-QuestPro-v0",
    entry_point="nle.minihack.envs.skills_quest:MiniHackQuestPro",
)
