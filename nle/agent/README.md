# Using The Baselines

In this README we describe how to use the baselines implemented here to
reproduce the results of the MiniHack paper. This assumes you've installed `nle` and `minihack`.

## Installing agent requirements

We provide two baseline agent implementations.
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
  provided in `nle.agent.rllib`, with a similar model to the TorchBeast agent.
  This can be used to try out a variety of different RL algorithms - several
  examples are provided. To install and train this agent use the following
  commands:
```bash
$ pip install "nle[rllib_agent]"
$ python -m nle.agent.rllib.train --algo=ppo
```

## Running experiments
