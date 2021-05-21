import os
from collections.abc import Iterable
from numbers import Number

import hydra
import numpy as np
import ray
import ray.tune.integration.wandb
from nle.agent.rllib.envs import RLLibNLEEnv  # noqa: F401
from nle.agent.rllib.models import RLLibNLENetwork  # noqa: F401
from omegaconf import DictConfig, OmegaConf
from ray import tune
from ray.rllib.agents import dqn, impala, ppo, a3c
from ray.tune.integration.wandb import (
    _VALID_ITERABLE_TYPES,
    _VALID_TYPES,
    WandbLoggerCallback,
)
from ray.tune.utils import merge_dicts


# Hacky monkey-patching to allow for OmegaConf config
def _is_allowed_type(obj):
    """Return True if type is allowed for logging to wandb"""
    if isinstance(obj, DictConfig):
        return True
    if isinstance(obj, np.ndarray) and obj.size == 1:
        return isinstance(obj.item(), Number)
    if isinstance(obj, Iterable) and len(obj) > 0:
        return isinstance(obj[0], _VALID_ITERABLE_TYPES)
    return isinstance(obj, _VALID_TYPES)


ray.tune.integration.wandb._is_allowed_type = _is_allowed_type


def get_full_config(cfg: DictConfig) -> DictConfig:
    env_flags = OmegaConf.to_container(cfg)
    max_num_steps = 1e6
    if cfg.env in ("staircase", "pet"):
        max_num_steps = 1000
    env_flags["max_num_steps"] = int(max_num_steps)
    env_flags["seedspath"] = ""
    return OmegaConf.create(env_flags)


NAME_TO_TRAINER: dict = {
    "impala": (impala, impala.ImpalaTrainer),
    "a2c": (a3c, a3c.A2CTrainer),
    "dqn": (dqn, dqn.DQNTrainer),
    "ppo": (ppo, ppo.PPOTrainer),
}


@hydra.main(config_name="config")
def train(cfg: DictConfig) -> None:
    ray.init(num_gpus=cfg.num_gpus, num_cpus=cfg.num_cpus + 1)
    cfg = get_full_config(cfg)

    try:
        algo, trainer = NAME_TO_TRAINER[cfg.algo]
    except KeyError:
        raise ValueError(
            "The algorithm you specified isn't currently supported: %s", cfg.algo
        )

    config = algo.DEFAULT_CONFIG.copy()

    # Generic Configuration
    config.update(
        {
            "framework": "torch",
            "num_gpus": cfg.num_gpus,
            "seed": cfg.seed,
            "env": "rllib_nle_env",
            "env_config": {
                "flags": cfg,
                "observation_keys": cfg.obs_keys.split(","),
                "name": cfg.env,
            },
            "train_batch_size": cfg.train_batch_size,
            "model": {
                "custom_model": "rllib_nle_model",
                "custom_model_config": {"flags": cfg, "algo": cfg.algo},
                "use_lstm": cfg.use_lstm,
                "lstm_use_prev_reward": True,
                "lstm_use_prev_action": True,
                "lstm_cell_size": cfg.hidden_dim,  # same as h_dim in models.NetHackNet
            },
            "num_workers": cfg.num_cpus,
            "num_envs_per_worker": int(cfg.num_actors / cfg.num_cpus),
            "evaluation_interval": 100,
            "evaluation_num_episodes": 50,
            "evaluation_config": {"explore": False},
            "rollout_fragment_length": cfg.unroll_length,
        }
    )

    # Algo-specific config. Requires hydra config keys to match rllib exactly
    algo_config = OmegaConf.to_container(cfg[cfg.algo])
    config = merge_dicts(config, algo_config)

    callbacks = []
    if cfg.wandb:
        callbacks.append(
            WandbLoggerCallback(
                project=cfg.project,
                api_key_file="~/.wandb_api_key",
                entity=cfg.entity,
                group=cfg.group,
                tags=cfg.tags.split(","),
            )
        )
        os.environ["TUNE_DISABLE_AUTO_CALLBACK_LOGGERS"] = "1"  # Only log to wandb

    tune.run(
        trainer,
        stop={"timesteps_total": cfg.total_steps},
        config=config,
        name=cfg.name,
        callbacks=callbacks,
    )


if __name__ == "__main__":
    train()
