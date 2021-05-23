import threading

from nle.env import tasks as nle_tasks
from nle.minihack import MiniHack
from nle.minihack.envs import (
    corridor,
    keyroom,
    mazewalk,
    minigrid,
    room,
    boxohack,
    fightcorridor,
    river,
    memento,
    hidenseek,
    deepexplore,
    skills_simple,
    skills_levitate,
    skills_wod,
)
from nle.agent.common.envs.wrapper import CounterWrapper, CropWrapper, PrevWrapper


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
    mazewalk_huge=mazewalk.MiniHackMazeWalk45x19,
    mazewalk_huge_mapped=mazewalk.MiniHackMazeWalk45x19Premapped,
    # MiniHack Fight Corridor
    fight_corridor=fightcorridor.MiniHackFightCorridor,
    fight_corridor_dark=fightcorridor.MiniHackFightCorridorDark,
    # MiniHack River
    river=river.MiniHackRiver,
    river_lava=river.MiniHackRiverLava,
    river_monster=river.MiniHackRiverMonster,
    river_monsterlava=river.MiniHackRiverMonsterLava,
    river_narrow=river.MiniHackRiverNarrow,
    # MiniHack Memento
    memento_short=memento.MiniHackMementoShortF2,
    memento=memento.MiniHackMementoF2,
    memento_hard=memento.MiniHackMementoF4,
    # MiniHack Hide&Seek
    hidenseek=hidenseek.MiniHackHideAndSeek,
    hidenseek_mapped=hidenseek.MiniHackHideAndSeekMapped,
    hidenseek_lava=hidenseek.MiniHackHideAndSeekLava,
    hidenseek_big=hidenseek.MiniHackHideAndSeekBig,
    # MiniHack Harvest/DeepExplore
    harvest2=deepexplore.MiniHackDeepExplore2,
    harvest3=deepexplore.MiniHackDeepExplore3,
    harvest5=deepexplore.MiniHackDeepExplore5,
    harvest8=deepexplore.MiniHackDeepExplore8,
    # MiniHack MultiRooms
    multiroom_2=minigrid.MiniHackMultiRoomN2,
    multiroom_4=minigrid.MiniHackMultiRoomN4,
    multiroom_6=minigrid.MiniHackMultiRoomN6,
    multiroom_2_locked=minigrid.MiniHackMultiRoomN2Locked,
    multiroom_4_locked=minigrid.MiniHackMultiRoomN4Locked,
    multiroom_6_locked=minigrid.MiniHackMultiRoomN6Locked,
    multiroom_2_lava=minigrid.MiniHackMultiRoomN2Lava,
    multiroom_4_lava=minigrid.MiniHackMultiRoomN4Lava,
    multiroom_6_lava=minigrid.MiniHackMultiRoomN6Lava,
    multiroom_2_monster=minigrid.MiniHackMultiRoomN2Monster,
    multiroom_4_monster=minigrid.MiniHackMultiRoomN4Monster,
    multiroom_6_monster=minigrid.MiniHackMultiRoomN6Monster,
    multiroom_2_extreme=minigrid.MiniHackMultiRoomN2Extreme,
    multiroom_4_extreme=minigrid.MiniHackMultiRoomN4Extreme,
    multiroom_6_extreme=minigrid.MiniHackMultiRoomN6Extreme,
    # MiniHack Boxoban
    boxoban_hard=boxohack.MiniHackBoxobanHard,
    boxoban_medium=boxohack.MiniHackBoxobanMedium,
    # MiniHack Skills
    mini_eat=skills_simple.MiniHackEat,
    mini_pray=skills_simple.MiniHackPray,
    mini_sink=skills_simple.MiniHackSink,
    mini_closed=skills_simple.MiniHackClosedDoor,
    mini_locked=skills_simple.MiniHackLockedDoor,
    mini_read=skills_simple.MiniHackRead,
    mini_zap=skills_simple.MiniHackZap,
    mini_puton=skills_simple.MiniHackPutOn,
    mini_wear=skills_simple.MiniHackWear,
    mini_wield=skills_simple.MiniHackWield,
    # WoD
    wod_easy=skills_wod.MiniHackWoDEasy,
    wod_medium=skills_wod.MiniHackWoDMedium,
    wod_hard=skills_wod.MiniHackWoDHard,
    wod_pro=skills_wod.MiniHackWoDPro,
    # MiniHack Levitat
    levitate_boot=skills_levitate.MiniHackLevitateBoots,
    levitate_ring=skills_levitate.MiniHackLevitateRing,
    levitate_potion=skills_levitate.MiniHackLevitatePotion,
    levitate_random=skills_levitate.MiniHackLevitateRandom,
)


def is_env_minihack(env_cls):
    return issubclass(env_cls, MiniHack)


def create_env(flags, env_id=0, lock=threading.Lock()):
    # Create environment instances for actors
    with lock:
        env_class = ENVS[flags.env]
        if flags.model == "tty":
            observation_keys = ("tty_chars", "tty_colors", "tty_cursor", "blstats")
        else:
            observation_keys = flags.obs_keys.split(",")
        kwargs = dict(
            savedir=None,
            archivefile=None,
            observation_keys=observation_keys,
            penalty_step=flags.penalty_step,
            penalty_time=flags.penalty_time,
            penalty_mode=flags.fn_penalty_step,
        )
        if not is_env_minihack(env_class):
            kwargs.update(max_episode_steps=flags.max_num_steps)
            kwargs.update(character=flags.character)
        # if flags.env in ("staircase", "pet", "oracle"):
        #     kwargs.update(reward_win=flags.reward_win, reward_lose=flags.reward_lose)
        elif env_id == 0:
            # print("Ignoring flags.reward_win and flags.reward_lose")
            pass
        env = env_class(**kwargs)
        if flags.state_counter != "none":
            env = CounterWrapper(env, flags.state_counter)
        if flags.model == "tty":
            env = CropWrapper(env)
            env = PrevWrapper(env)
        if flags.seedspath is not None and len(flags.seedspath) > 0:
            raise NotImplementedError("seedspath > 0 not implemented yet.")

        return env
