import torch

from nle.agent.polybeast.models.base import BaseNet
from nle.agent.polybeast.skill_transfer.skill_transfer import load_model


class FOCNet(BaseNet):
    def __init__(self, observation_shape, num_actions, flags, device):
        NUM_OPTIONS = 2

        super(FOCNet, self).__init__(observation_shape, NUM_OPTIONS, flags, device)

        options_path = flags.foc_options_path.split(" ")
        configs_path = flags.foc_options_config_path.split(" ")

        if len(options_path) != len(configs_path):
            raise ValueError(
                "options_path length does not equal configs_length "
                + str(len(options_path))
                + " "
                + str(len(configs_path))
            )

        self.num_options = len(options_path)

        self.options = [
            load_model(flags.env, paths[0], paths[1])[0]
            for paths in zip(options_path, configs_path)
        ]

    def forward(self, inputs, core_state, learning=False):
        (output, core_state) = super().forward(inputs, core_state, learning)
        # TODO Think about recurrent state for the options

        with torch.no_grad():
            option_outs = [
                self.options[i](inputs, core_state, learning)
                for i in range(len(self.options))
            ]

        action = []
        batch_size = output["policy_logits"].shape[0]

        for i in range(batch_size):
            action.append(
                option_outs[output["action"][i]][0]["action"][i].unflatten(
                    dim=0, sizes=(1, -1)
                )
            )

        action = torch.cat(action, dim=0)

        return (
            dict(
                policy_logits=output["policy_logits"],
                baseline=output["baseline"],
                action=action,
                extra_data=output["action"],
            ),
            core_state,
        )
