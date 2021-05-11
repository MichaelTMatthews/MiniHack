import os

import hydra
import ray
from nle.agent.rllib.envs import RLLibNLEEnv  # noqa: F401
from nle.agent.rllib.models import RLLibNLENetwork  # noqa: F401
from omegaconf import DictConfig, OmegaConf
from ray import tune
from ray.rllib.agents import impala
from ray.tune.integration.wandb import WandbLoggerCallback


def get_full_config(cfg: DictConfig) -> DictConfig:
    env_flags = OmegaConf.to_container(cfg)
    max_num_steps = 1e6
    if cfg.env in ("staircase", "pet"):
        max_num_steps = 1000
    env_flags["max_num_steps"] = int(max_num_steps)
    env_flags["seedspath"] = ""
    return OmegaConf.create(env_flags)


@hydra.main(config_name="config")
def train(cfg: DictConfig) -> None:
    ray.init(num_gpus=cfg.num_gpus, num_cpus=cfg.num_cpus + 1)
    cfg = get_full_config(cfg)

    config = impala.DEFAULT_CONFIG.copy()
    config.update(
        {
            "framework": "torch",
            "num_gpus": cfg.num_gpus,
            "seed": cfg.seed,
            "env": "rllib_nle_env",
            "env_config": {
                "flags": cfg,
                "observation_keys": cfg.obs_keys.split(","),
            },
            "train_batch_size": cfg.batch_size,
            "model": {
                "custom_model": "rllib_nle_model",
                "custom_model_config": {"flags": cfg},
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
            "entropy_coeff": cfg.entropy_cost,
            "vf_loss_coeff": cfg.baseline_cost,
            "rollout_fragment_length": cfg.unroll_length,
            "grad_clip": cfg.grad_norm_clip,
            "gamma": cfg.discounting,
            "lr": cfg.learning_rate,
            "decay": cfg.alpha,
            "momentum": cfg.momentum,
            "epsilon": cfg.epsilon,
        }
    )
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
        impala.ImpalaTrainer,
        stop={"timesteps_total": cfg.total_steps},
        config=config,
        name=cfg.name,
        callbacks=callbacks,
    )


if __name__ == "__main__":
    train()
