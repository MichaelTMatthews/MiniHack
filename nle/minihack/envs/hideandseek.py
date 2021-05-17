from nle.minihack import MiniHack, MiniHackSkill
from gym.envs import registration


class MiniHackHideAndSeek(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        des_file = """
MAZE: "mylevel", ' '
FLAGS:hardfloor
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
$place = { (10,8),(0,8),(10,0) }
SHUFFLE: $place
REGION:(0,0,11,9),lit,"ordinary"
BRANCH:(0,0,1,1),(2,2,2,2)
STAIR:$place[0],down
$monster = monster: { 'L','N','H','O','D','T' }
SHUFFLE: $monster
MONSTER: $monster[0], $place[1], hostile
REPLACE_TERRAIN:(0,0,11,9), '.', 'C', 33%
REPLACE_TERRAIN:(0,0,11,9), '.', 'T', 25%
TERRAIN:randline (0,9),(11,0), 5, '.'
TERRAIN:randline (0,0),(11,9), 5, '.'
"""
        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-HideAndSeek-v0",
    entry_point="nle.minihack.envs.hideandseek:MiniHackHideAndSeek",
)
