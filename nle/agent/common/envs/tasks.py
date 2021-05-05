import threading
from collections import defaultdict

import numpy as np
from nle.env import tasks as nle_tasks
from nle.minihack import MiniHack
from nle.minihack.envs import corridor, keyroom, mazewalk, minigrid, room


class SharedPatch(object):
    def __init__(self, *args, state_counter="none", **kwargs):
        # intialize state counter
        self.state_counter = state_counter
        if self.state_counter != "none":
            self.state_count_dict = defaultdict(int)
        # this super() goes to the parent of the particular task, not to `object`
        super().__init__(*args, **kwargs)

    def step(self, action):
        # add state counting to step function if desired
        step_return = super().step(action)
        if self.state_counter == "none":
            # do nothing
            return step_return

        obs, reward, done, info = step_return

        if self.state_counter == "ones":
            # treat every state as unique
            state_visits = 1
        elif self.state_counter == "coordinates":
            # use the location of the agent within the dungeon to accumulate visits
            features = obs["blstats"]
            x = features[0]
            y = features[1]
            # TODO: prefer to use dungeon level and dungeon number from Blstats
            d = features[12]
            coord = (d, x, y)
            self.state_count_dict[coord] += 1
            state_visits = self.state_count_dict[coord]
        else:
            raise NotImplementedError("state_counter=%s" % self.state_counter)

        obs.update(state_visits=np.array([state_visits]))

        if done:
            self.state_count_dict.clear()

        return step_return

    def reset(self, wizkit_items=None):
        # reset state counter when env resets
        obs = super().reset(wizkit_items=wizkit_items)
        if self.state_counter != "none":
            self.state_count_dict.clear()
            # current state counts as one visit
            obs.update(state_visits=np.array([1]))
        return obs


class PatchedNetHackScore(SharedPatch, nle_tasks.NetHackScore):
    pass


class PatchedNetHackStaircase(SharedPatch, nle_tasks.NetHackStaircase):
    def __init__(self, *args, reward_win=1, reward_lose=-1, **kwargs):
        super().__init__(*args, **kwargs)
        self.reward_win = reward_win
        self.reward_lose = reward_lose

    def _reward_fn(self, last_response, response, end_status):
        if end_status == self.StepStatus.TASK_SUCCESSFUL:
            reward = self.reward_win
        elif end_status == self.StepStatus.RUNNING:
            reward = 0
        else:  # death or aborted
            reward = self.reward_lose
        return reward + self._get_time_penalty(last_response, response)


class PatchedNetHackStaircasePet(
    PatchedNetHackStaircase, nle_tasks.NetHackStaircasePet
):
    pass  # inherit from PatchedNetHackStaircase


class PatchedNetHackStaircaseOracle(PatchedNetHackStaircase, nle_tasks.NetHackOracle):
    pass  # inherit from PatchedNetHackStaircase


class PatchedNetHackGold(SharedPatch, nle_tasks.NetHackGold):
    pass


class PatchedNetHackEat(SharedPatch, nle_tasks.NetHackEat):
    pass


class PatchedNetHackScout(SharedPatch, nle_tasks.NetHackScout):
    pass


NetHackScore = PatchedNetHackScore
NetHackStaircase = PatchedNetHackStaircase
NetHackStaircasePet = PatchedNetHackStaircasePet
NetHackOracle = PatchedNetHackStaircaseOracle
NetHackGold = PatchedNetHackGold
NetHackEat = PatchedNetHackEat
NetHackScout = PatchedNetHackScout


ENVS = dict(
    # NLE tasks
    staircase=nle_tasks.NetHackStaircase,
    score=nle_tasks.NetHackScore,
    pet=nle_tasks.NetHackStaircasePet,
    oracle=nle_tasks.NetHackOracle,
    gold=nle_tasks.NetHackGold,
    eat=nle_tasks.NetHackEat,
    scout=nle_tasks.NetHackScout,
    # MiniHack Room
    small_room=room.MiniHackRoom5x5,
    small_room_random=room.MiniHackRoom5x5Random,
    small_room_dark=room.MiniHackRoom5x5Dark,
    small_room_monster=room.MiniHackRoom5x5Monster,
    small_room_trap=room.MiniHackRoom5x5Trap,
    big_room=room.MiniHackRoom15x15,
    big_room_random=room.MiniHackRoom15x15Random,
    big_room_dark=room.MiniHackRoom15x15Dark,
    big_room_monster=room.MiniHackRoom15x15Monster,
    big_room_monster_trap=room.MiniHackRoom15x15MonsterTrap,
    # MiniHack Corridor
    corridor2=corridor.MiniHackCorridor2,
    corridor3=corridor.MiniHackCorridor3,
    corridor5=corridor.MiniHackCorridor5,
    corridor8=corridor.MiniHackCorridor8,
    corridor10=corridor.MiniHackCorridor10,
    # MiniHack KeyRoom
    keyroom_small_fixed=keyroom.MiniHackKeyRoom5x5Fixed,
    keyroom_small=keyroom.MiniHackKeyRoom5x5,
    keyroom_small_dark=keyroom.MiniHackKeyRoom5x5Dark,
    keyroom_big=keyroom.MiniHackKeyRoom15x15,
    keyroom_big_dark=keyroom.MiniHackKeyRoom15x15Dark,
    # MiniHack MazeWalk
    mazewalk_small=mazewalk.MiniHackMazeWalk9x9,
    mazewalk_small_mapped=mazewalk.MiniHackMazeWalk9x9Premapped,
    mazewalk_big=mazewalk.MiniHackMazeWalk15x15,
    mazewalk_big_mapped=mazewalk.MiniHackMazeWalk15x15Premapped,
    mazewalk_huge=mazewalk.MiniHackMazeWalkMax,
    mazewalk_huge_mapped=mazewalk.MiniHackMazeWalkMaxPremapped,
    # MiniHack MultiRooms
    multiroom_2=minigrid.MiniHackMultiRoomN2,
    multiroom_4=minigrid.MiniHackMultiRoomN4,
    multiroom_6=minigrid.MiniHackMultiRoomN6,
    multiroom_2_locked=minigrid.MiniHackMultiRoomN2Locked,
    multiroom_4_locked=minigrid.MiniHackMultiRoomN4Locked,
    multiroom_6_locked=minigrid.MiniHackMultiRoomN6Locked,
    multiroom_2_trap=minigrid.MiniHackMultiRoomN2Trap,
    multiroom_4_trap=minigrid.MiniHackMultiRoomN4Trap,
    multiroom_6_trap=minigrid.MiniHackMultiRoomN6Trap,
    multiroom_2_monster=minigrid.MiniHackMultiRoomN2Monster,
    multiroom_4_monster=minigrid.MiniHackMultiRoomN4Monster,
    multiroom_6_monster=minigrid.MiniHackMultiRoomN6Monster,
    multiroom_2_extreme=minigrid.MiniHackMultiRoomN2Extreme,
    multiroom_4_extreme=minigrid.MiniHackMultiRoomN4Extreme,
    multiroom_6_extreme=minigrid.MiniHackMultiRoomN6Extreme,
)


def is_env_minihack(env_cls):
    return issubclass(env_cls, MiniHack)


def create_env(flags, env_id=0, lock=threading.Lock()):
    # Create environment instances for actors
    with lock:
        env_class = ENVS[flags.env]
        kwargs = dict(
            savedir=None,
            archivefile=None,
            character=flags.character,
            observation_keys=flags.obs_keys.split(","),
            penalty_step=flags.penalty_step,
            penalty_time=flags.penalty_time,
            penalty_mode=flags.fn_penalty_step,
        )
        if not is_env_minihack(env_class):
            kwargs.update(max_episode_steps=flags.max_num_steps)
        if flags.env in ("staircase", "pet", "oracle"):
            kwargs.update(reward_win=flags.reward_win, reward_lose=flags.reward_lose)
        elif env_id == 0:
            # removed as too noisy
            # print("Ignoring flags.reward_win and flags.reward_lose")
            pass
        if flags.state_counter != "none":
            kwargs.update(state_counter=flags.state_counter)
        env = env_class(**kwargs)
        if flags.seedspath is not None and len(flags.seedspath) > 0:
            raise NotImplementedError("seedspath > 0 not implemented yet.")

        return env
