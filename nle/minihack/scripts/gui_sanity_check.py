from nle.minihack import MiniHackSkillEnv, LevelGenerator


class MiniHackGUITest(MiniHackSkillEnv):
    """Environment for "eat" task."""

    def __init__(self, *args, obs_crop_h=5, obs_crop_w=5, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_stair_up((2, 2))

        lvl_gen.add_object("apple", "%", place=(0, 0))
        lvl_gen.add_object("pear", "%", place=(0, 1))
        lvl_gen.add_object("dagger", ")", place=(0, 2))
        lvl_gen.add_object("robe", "[", place=(0, 3))
        lvl_gen.add_object("boulder", "`", place=(0, 4))

        lvl_gen.add_terrain((1, 1), "W")  # water
        lvl_gen.add_terrain((1, 1), "L")  # lava
        lvl_gen.add_terrain((1, 1), "T")  # tree
        lvl_gen.add_terrain((1, 1), "{")  # fountain
        lvl_gen.add_terrain((1, 1), "#")  # iron bars

        lvl_gen.add_terrain((4, 0), "|")
        lvl_gen.add_terrain((4, 1), "|")
        lvl_gen.add_terrain((4, 2), "|")
        lvl_gen.add_terrain((4, 3), "|")
        lvl_gen.add_terrain((4, 4), "|")
        lvl_gen.add_door("open", place=(4, 1))
        lvl_gen.add_door("closed", place=(4, 4))

        lvl_gen.add_monster("killer bee", place=(3, 0))
        lvl_gen.add_monster("oracle", place=(3, 1))
        lvl_gen.add_monster("tiger", place=(3, 2))
        lvl_gen.add_monster("minotaur", place=(3, 3))
        lvl_gen.add_monster("black dragon", place=(3, 4))

        des_file = lvl_gen.get_des()

        kwargs["observation_keys"] = (
            "glyphs_crop",
            "screen_descriptions_crop",
        )

        super().__init__(*args, des_file=des_file, **kwargs)


env = MiniHackGUITest()
obs = env.reset()

# Glyphs
print(obs["glyphs_crop"])
# Textual descriptions
screen_description = obs["screen_descriptions_crop"]
for i in range(screen_description.shape[0]):
    for j in range(screen_description.shape[1]):
        name = screen_description[i, j].tobytes().decode("utf-8")
        print(name)

env.render(mode="human")
