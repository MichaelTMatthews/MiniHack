# Copyright (c) Facebook, Inc. and its affiliates.
import os
import random

import numpy as np
import pkg_resources
from gym.envs import registration
from nle.minihack import LevelGenerator, MiniHackNavigation

LEVELS_PATH = os.path.join(
    pkg_resources.resource_filename("nle", "minihack/dat"), "boxoban-levels-master"
)


def load_boxoban_levels(cur_levels_path):
    levels = []
    for file in os.listdir(cur_levels_path):
        if file.endswith(".txt"):
            with open(os.path.join(cur_levels_path, file)) as f:
                cur_lines = f.readlines()
            cur_level = []
            for el in cur_lines:
                if el != "\n":
                    cur_level.append(el)
                else:
                    # 0th element is a level number, we don't need it
                    levels.append("".join(cur_level[1:]))
                    cur_level = []
    return levels


class BoxoHack(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 400)
        level_set = kwargs.pop("level_set", "unfiltered")
        level_mode = kwargs.pop("level_mode", "train")

        cur_levels_path = os.path.join(LEVELS_PATH, level_set, level_mode)

        self._flags = tuple(kwargs.pop("flags", []))
        self._levels = load_boxoban_levels(cur_levels_path)
        self._reward_shaping_coefficient = kwargs.pop("reward_shaping_coefficient", 0.1)

        super().__init__(*args, des_file=self.get_lvl_gen().get_des(), **kwargs)

    def get_env_map(self, level):
        info = {"fountains": [], "boulders": []}
        level = level[:-1]
        for row in range(0, len(level)):
            for col in range(len(level[row])):
                if level[row][col] == "$":
                    info["boulders"].append((col, row))
                if level[row][col] == ".":
                    info["fountains"].append((col, row))
            if "@" in level[row]:
                py = level[row].index("@")
                level[row] = level[row].replace("@", ".")
                info["player"] = (py, row)
            level[row] = level[row].replace(" ", ".")
            level[row] = level[row].replace("#", "F")
            level[row] = level[row].replace("$", ".")
        return "\n".join(level), info

    def get_lvl_gen(self):
        level = random.choice(self._levels)
        level = level.split("\n")
        map, info = self.get_env_map(level)
        flags = list(self._flags)
        flags.append("noteleport")
        flags.append("premapped")
        lvl_gen = LevelGenerator(map=map, lit=True, flags=flags, solidfill=" ")
        for b in info["boulders"]:
            lvl_gen.add_boulder(b)
        for f in info["fountains"]:
            lvl_gen.add_fountain(f)
        lvl_gen.add_stair_up(info["player"])
        return lvl_gen

    def reset(self):
        self.update(self.get_lvl_gen().get_des())
        initial_obs = super().reset()
        self._goal_pos_set = self._object_positions(self.last_observation, "{")
        return initial_obs

    def _is_episode_end(self, observation):
        # If every boulder is on a fountain, we're done
        if self._goal_pos_set == self._object_positions(observation, "`"):
            return self.StepStatus.TASK_SUCCESSFUL
        else:
            return self.StepStatus.RUNNING

    def _reward_fn(self, last_observation, observation, end_status):
        if end_status == self.StepStatus.TASK_SUCCESSFUL:
            return 1
        elif end_status != self.StepStatus.RUNNING:
            return 0
        return (
            self._count_boulders_on_fountains(observation)
            - self._count_boulders_on_fountains(last_observation)
        ) * self._reward_shaping_coefficient

    def _count_boulders_on_fountains(self, observation):
        return len(
            self._goal_pos_set.intersection(self._object_positions(observation, "`"))
        )

    def _object_positions(self, observation, object_char):
        char_obs = observation[self._original_observation_keys.index("chars")]
        return set((x, y) for x, y in zip(*np.where(char_obs == ord(object_char))))


class MiniHackBoxobanMedium(BoxoHack):
    def __init__(self, *args, **kwargs):
        kwargs["level_set"] = "medium"
        kwargs["level_mode"] = "train"
        super().__init__(*args, **kwargs)


class MiniHackBoxobanHard(BoxoHack):
    def __init__(self, *args, **kwargs):
        kwargs["level_set"] = "hard"
        kwargs["level_mode"] = ""
        super().__init__(*args, **kwargs)


registration.register(
    id="MiniHack-Boxoban-Medium-v0",
    entry_point="nle.minihack.envs.boxohack:MiniHackBoxobanMedium",
)

registration.register(
    id="MiniHack-Boxoban-Hard-v0",
    entry_point="nle.minihack.envs.boxohack:MiniHackBoxobanHard",
)
