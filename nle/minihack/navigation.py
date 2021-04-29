# Copyright (c) Facebook, Inc. and its affiliates.

from nle.minihack import MiniHack, LevelGenerator
from nle import nethack
from nle.nethack import Command


MOVE_ACTIONS = tuple(nethack.CompassDirection)
APPLY_ACTIONS = tuple(list(MOVE_ACTIONS) + [Command.PICKUP, Command.APPLY])
NAVIGATE_ACTIONS = tuple(
    list(MOVE_ACTIONS) + [Command.OPEN, Command.KICK, Command.SEARCH]
)


class MiniHackNavigation(MiniHack):
    """Base class for maze-type task.

    Maze environments have
    - Restricted action space (move only by default)
    - No pet
    - One-letter menu questions are NOT allowed by default
    - Restricted observations, only glyphs by default
    - No random monster generation

    The goal is to reach the staircase.
    """

    def __init__(self, *args, des_file: str = None, **kwargs):
        # No pet
        kwargs["options"] = kwargs.pop("options", list(nethack.NETHACKOPTIONS))
        kwargs["options"].append("pettype:none")
        # Actions space - move only
        kwargs["actions"] = kwargs.pop("actions", MOVE_ACTIONS)
        # Disallowing one-letter menu questions
        kwargs["allow_all_yn_questions"] = kwargs.pop("allow_all_yn_questions", False)
        # Override episode limit
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 100)
        # Restrict the observation space to glyphs only
        kwargs["observation_keys"] = kwargs.pop("observation_keys", ["chars_crop"])
        # No random monster generation after every timestep
        self._no_rand_mon()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackEmpty(MiniHackNavigation):
    """Environment for "empty" task."""

    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 50)
        size = kwargs.pop("size", 5)
        random = kwargs.pop("random", True)

        lvl_gen = LevelGenerator(w=size, h=size, lit=True)
        if random:
            lvl_gen.add_stair_down()
        else:
            lvl_gen.add_stair_down((size - 1, size - 1))
            lvl_gen.add_stair_up((0, 0))

        super().__init__(*args, des_file=lvl_gen.get_des(), **kwargs)


class MiniHackCorridor(MiniHackNavigation):
    """Environment for "corridor" task.

    The agent has to navigate itself through randomely generated corridors that
    connect several rooms and find the goal.
    """

    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 1000)
        kwargs["actions"] = NAVIGATE_ACTIONS
        rooms = kwargs.pop("rooms", 2)
        assert rooms in [2, 3, 5, 8, 10]
        super().__init__(*args, des_file=f"corridor{rooms}.des", **kwargs)


class MiniHackMazeWalk(MiniHackNavigation):
    """Environment for "mazewalk" task."""

    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 1000)
        self._no_rand_mon()
        super().__init__(*args, des_file="mazewalk.des", **kwargs)


class MiniHackKeyDoor(MiniHackNavigation):
    """Environment for "key and door" task.

    This environment has a key that the agent must pick up in order to
    unlock a goal and then get to the green goal square. This environment
    is difficult, because of the sparse reward, to solve using classical
    RL algorithms. It is useful to experiment with curiosity or curriculum
    learning.
    """

    def __init__(self, *args, **kwargs):
        kwargs["options"] = kwargs.pop("options", list(nethack.NETHACKOPTIONS))
        kwargs["options"].append("!autopickup")
        kwargs["character"] = kwargs.pop("charachter", "rog-hum-cha-mal")
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 200)
        kwargs["actions"] = APPLY_ACTIONS
        super().__init__(*args, des_file="key_and_door.des", **kwargs)

    def step(self, action: int):
        # If apply action is chosen
        if self._actions[action] == Command.APPLY:
            key_key = self.key_in_inventory("key")
            # if key is in the inventory
            if key_key is not None:
                # Check if there is a closed door nearby
                dir_key = self.get_direction_obj("closed door")
                if dir_key is not None:
                    # Perform the following NetHack steps
                    self.env.step(Command.APPLY)  # press apply
                    self.env.step(ord(key_key))  # choose key from the inv
                    self.env.step(dir_key)  # select the door's direction
                    obs, done = self.env.step(ord("y"))  # press y
                    obs, done = self._perform_known_steps(obs, done, exceptions=True)
                    # Make sure the door is open
                    while True:
                        obs, done = self.env.step(dir_key)
                        obs, done = self._perform_known_steps(
                            obs, done, exceptions=True
                        )
                        if self.get_direction_obj("closed door", obs) is None:
                            break

        obs, reward, done, info = super().step(action)
        return obs, reward, done, info
