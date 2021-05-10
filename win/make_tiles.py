import os
import re
import json

FILES = ["monsters.txt", "objects.txt", "other.txt"]
DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "share")
OUT_FILE = "tiles.json"
PATTERN = re.compile(r"^# tile (\d+) \((.*?)\)$", re.MULTILINE)

id_to_tile = []

for fn in FILES:
    print("Reading {}".format(fn))
    with open(os.path.join(DIR, fn)) as f:
        lines = f.readlines()

    i = 0
    ind = 0
    max_line = len(lines)
    while i < max_line:
        line = lines[i]
        if re.match(PATTERN, line):
            tile = "".join(lines[i + 2 : i + 18])
            tile = tile.replace(" ", "")
            id_to_tile.append(tile)
            ind += 1

        i += 1

with open(OUT_FILE, "w") as outf:
    json.dump(id_to_tile, outf)
