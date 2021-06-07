# MiniHack the Planet: A Sandbox for Open-Ended Reinforcement Learning Research

```
        <                                                
        ###                                              
         ###                                             
          ###                                            
           ###            ##########                     
            ###       #################                  
              ##  #  ###             ####                
               ###  ##    ###### ###   ##                
              # #####    ###    ####   ###               
                  ##    ###     ###    ###               
                  ##   ###      ###    ###               
                  ##   ###      ###    ##                
                  ##   ###     ###   ###                 
                  ###   ###############                  
                   ###                 ##>               
                     #####          #####                
                       ###############                   
                            ##### 
```

MiniHack is a sandbox framework for easily designing environments for
Reinforcement Learning. MiniHack is based on the [The NetHack Learning
Environment (NLE)](https://github.com/facebookresearch/nle) and provides a
standard RL interface for customly created tesbeds.

NetHack is one of the oldest and arguably most impactful videogames in history,
as well as being one of the hardest roguelikes currently being played by humans.
It is procedurally generated, rich in entities and dynamics, and overall an
extremely challenging environment for current state-of-the-art RL agents, while
being much cheaper to run compared to other challenging testbeds. Through NLE,
we wish to establish NetHack as one of the next challenges for research in
decision making and machine learning.

You can read more about NLE in the [NeurIPS 2020
paper](https://arxiv.org/abs/2006.13760), and about NetHack in its [original
README](./README.nh), at [nethack.org](https://nethack.org/), and on the
[NetHack wiki](https://nethackwiki.com).

MiniHack, NLE and NetHack use [NETHACK GENERAL PUBLIC LICENSE](https://github.com/facebookresearch/nle/blob/master/LICENSE).

<!-- # Papers using the MiniHack The Planet
- Samvelyan et al. [MiniHack The Planet](https://arxiv.org/abs/20XX.YYYY) (FAIR, UCL, Oxford)

Open a [pull request](https://github.com/facebookresearch/nle/edit/master/README.md) to add papers -->

# Getting started

Starting with MiniHack environments is extremely simple, provided one is familiar
with other gym / RL environments.

## Installation

NLE requires `python>=3.5`, `cmake>=3.14` to be installed and available both when building the
package, and at runtime.

On **MacOS**, one can use `Homebrew` as follows:

``` bash
$ brew install cmake
```

On a plain **Ubuntu 18.04** distribution, `cmake` and other dependencies
can be installed by doing:

```bash
# Python and most build deps
$ sudo apt-get install -y build-essential autoconf libtool pkg-config \
    python3-dev python3-pip python3-numpy git flex bison libbz2-dev

# recent cmake version
$ wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | sudo apt-key add -
$ sudo apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main'
$ sudo apt-get update && apt-get --allow-unauthenticated install -y \
    cmake \
    kitware-archive-keyring
```

Afterwards it's a matter of setting up your environment. We advise using a conda
environment for this:

```bash
$ conda create -n nle python=3.8
$ conda activate nle
$ pip install nle
```


NOTE: If you want to extend / develop NLE, please install the package as follows:

``` bash
$ git clone https://github.com/MiniHackPlanet/MiniHack --recursive
$ pip install -e ".[dev]"
$ pre-commit install
```


## Trying it out

After installation, one can try out any of the provided tasks as follows:

```python
>>> import gym
>>> import nle
>>> env = gym.make("MiniHack-Eat-v0")
>>> env.reset()  # each reset generates a new dungeon
>>> env.step(1)  # move agent '@' north
>>> env.render()
```

MiniHack also comes with a few scripts that allow to get some environment rollouts,
and play with the action space:

```bash
# Play the MiniHack in the Terminal as a human
$ python -m nle.scripts.play --env MiniHack-River-v0

# Use a random agent
$ python -m nle.scripts.play --env MiniHack-River-v0  --mode random

# See all the options
$ python -m nle.scripts.play --help

# Play the MiniHack with graphical user interface (gui)
$ python -m nle.scripts.play_gui --env MiniHack-River-v0
```

Note that `nle.scripts.play` can also be run with `nle-play`, if the package
has been properly installed.

MiniHack comes with a set of predefined set of tasks. For the full list see [here](./TASKS.md)

## Baseline Agents

Several baseline agents are included as part of MiniHack, which can be
installed and used as follows:

* a [TorchBeast](https://github.com/facebookresearch/torchbeast) agent is
  bundled in `nle.agent.polybeast` together with a simple model to provide
  a starting point for experiments. To install and train this agent, first
  install torchbeast be following the instructions
  [here](https://github.com/facebookresearch/torchbeast#installing-polybeast),
  then use the following commands:
``` bash
$ pip install "nle[polybeast_agent]"
$ python -m nle.agent.polybeast.polyhydra --num_actors=80 --batch_size=32 --unroll_length=80 --learning_rate=0.0001 --entropy_cost=0.0001 --use_lstm=true --total_steps=1000000000
```

* An [RLlib](https://github.com/ray-project/ray#rllib-quick-start) agent is
  provided in `nle.agent.rllib`, with a similar model to the torchbeast agent.
  This can be used to try out a variety of different RL algorithms - several
  examples are provided. To install and train this agent use the following
  commands:
```bash
$ pip install "nle[rllib_agent]"
$ python -m nle.agent.rllib.train --algo=ppo
```

More information on running these agents, and instructions on how to reproduce
the results of the MiniHack paper, can be found in [this
document](./nle/agent/README.md).

# Contributing

We welcome contributions to MiniHack. If you are interested in contributing please 
see [this document](./CONTRIBUTING.md) 

# Citation
<!-- 
If you use MiniHack in any of your work, please cite:

```
@inproceedings{kuettler2020nethack,
  author    = {Heinrich K{\"{u}}ttler and
               Nantas Nardelli and
               Alexander H. Miller and
               Roberta Raileanu and
               Marco Selvatici and
               Edward Grefenstette and
               Tim Rockt{\"{a}}schel},
  title     = {{The NetHack Learning Environment}},
  booktitle = {Proceedings of the Conference on Neural Information Processing Systems (NeurIPS)},
  year      = {2020},
}
```
 -->
If you use MiniHack's interface on environments ported from other benchmarks, please cite the original paper as well:

- [MiniGrid](https://github.com/maximecb/gym-minigrid/) (see [LICENSE](https://github.com/maximecb/gym-minigrid/blob/master/LICENSE))

```
@misc{gym_minigrid,
  author = {Chevalier-Boisvert, Maxime and Willems, Lucas and Pal, Suman},
  title = {Minimalistic Gridworld Environment for OpenAI Gym},
  year = {2018},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/maximecb/gym-minigrid}},
}
```

- [Boxoban](https://github.com/deepmind/boxoban-levels/) (see [LICENSE](https://github.com/deepmind/boxoban-levels/blob/master/LICENSE))

```
@misc{boxobanlevels,
  author = {Arthur Guez, Mehdi Mirza, Karol Gregor, Rishabh Kabra, Sebastien Racaniere, Theophane Weber, David Raposo, Adam Santoro, Laurent Orseau, Tom Eccles, Greg Wayne, David Silver, Timothy Lillicrap, Victor Valdes},
  title = {An investigation of Model-free planning: boxoban levels},
  howpublished= {https://github.com/deepmind/boxoban-levels/},
  year = "2018",
}
```
