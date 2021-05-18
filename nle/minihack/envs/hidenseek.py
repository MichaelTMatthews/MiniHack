from nle.minihack import MiniHackNavigation
from gym.envs import registration

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
REPLACE_TERRAIN:(0,0,11,9), '.', 'C', 33%
REPLACE_TERRAIN:(0,0,11,9), '.', 'T', 25%
TERRAIN:randline (0,9),(11,0), 5, '.'
TERRAIN:randline (0,0),(11,9), 5, '.'
$monster = monster: { 'L','N','H','O','D','T' }
SHUFFLE: $monster
MONSTER: $monster[0], $place[0], hostile
BRANCH:(0,0,0,0),(1,1,1,1)
STAIR:$place[2],down
"""


class MiniHackHideAndSeek(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 1000)
        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-HnS-v0",
    entry_point="nle.minihack.envs.skills_quest:MiniHackHideAndSeek",
)
