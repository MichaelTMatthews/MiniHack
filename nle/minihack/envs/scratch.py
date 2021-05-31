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
      WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
      WWWWWWWWWWWWWWWWWWIIWWWIIIIWWWWWWWWWWWWWWWIWWWWWWWWWWWWWWWWWWWWWW
      WWWWWWWWWWWWWIIIIIWIIIIIIIIIWWWWWWIIIWWWWWWWWWWWWIIWWWWWWWWWWWWWW
      WWWWWWWWWW.....IIIWWWWIIIIIIWWWWWWWWWWWWWWIWW...........W...WWWWW
      ..W..................WWIIIWWW.WWWWW.TT........TTTTTT.............
      WW...WW..TTTTTT.WW...WWWWWWWWWWWW..W.TTTTT...TT.TTTTTTTTTTTWW.WWW
      WWWWWWWWW.TT..TTTTTTT.WWWWWWWWW.W......................TT.WW.WWWW
      WWWWWWWWWW........T.WWWWWWWWWWWW.W....W..W...............W.WWWWWW
      WWWWWWWWWWW.....TTWWWWWWWWWWWWW.WWWWWWW................WW.WWWWWWW
      WWWWWWWWWWWW...WWT.WWWWWWWWWWW.........W..WWW.........WWWWWWWWWWW
      WWWWWWWWWWWWWWW..WWWWWWWWWWWW...........W.WWWW.WWW..WW.WWWWWWWWWW
      WWWWWWWWWWWWWWWWWW.TTT.WWWWWWWWWW.TTTT...WWWWWWWWW..W.WWWWWWWWWWW
      WWWWWWWWWWWWWWWWWWTTTTTT..WWWWWWWW.TTT..WWWWWWWWWWWWWWWWWWW.WWWWW
      WWWWWWWWWWWWWWWWWWWWTTT..WWWWWWWWWW....W.WWWWWWWWWWWWW.....WWWWWW
      WWWWWWWWWWWWWWWWWWW.....WWWWWWWWWWW...WWWWWWWWWWWWWWWW......WWWWW
      WWWWWWWWWWWWWWWWWWW...WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW.WWWWWW
      WWWWWWWWWWWWWWWWWWW..WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW.W
      WWWWWWWWWWWWWWWWWWW.WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
      WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
      WWWWWWWWWWWWWWWWWWWWIIWWWWWWWWWWWWWWWWWWIIIIWWWIIIIIIIIIIIIIWWWWW
      WWWWWWWWIIIIIIIIIIIIIIWWWWWIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIWW
ENDMAP
STAIR:random,down
"""
        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-Scratch-v0",
    entry_point="nle.minihack.envs.scratch:MiniHackScratch",
)
