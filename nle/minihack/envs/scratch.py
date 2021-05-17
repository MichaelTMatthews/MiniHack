from nle.minihack import MiniHack, MiniHackSkill
from gym.envs import registration


class MiniHackScratchTmp(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        des_file = """
MAZE: "mylevel", ' '
FLAGS:hardfloor, premapped
INIT_MAP: solidfill,' '
GEOMETRY:center,center
MAP
-------------
|...........|
|...........|
|...........|
|...........|
|...........|
|...........|
|...........|
-------------
ENDMAP
TERRAIN:randline (1,1),(11,9),5, 'P'
"""
        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackScratch(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        des_file = """
MAZE: "mylevel", ' '
FLAGS:hardfloor, premapped
MESSAGE: "Welcome to MiniHack!"
INIT_MAP: solidfill,' '
GEOMETRY:center,center
MAP
...........
...........
...........
...........
...........
...........
...........
...........
...........
ENDMAP
$rivers = TERRAIN:{'L', 'W', 'I'}
SHUFFLE:$rivers
LOOP [2] {
  TERRAIN:randline (0,0),(11,9), 5, $rivers[0]
}
REPLACE_TERRAIN:(0,0,11,9), '.', 'T', 5%
STAIR:random,down
"""
        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-Scratch-v0",
    entry_point="nle.minihack.envs.scratch:MiniHackScratch",
)
