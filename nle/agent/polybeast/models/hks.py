import torch


from nle.agent.polybeast.models.base import BaseNet
from nle.agent.polybeast.skill_transfer.skill_transfer import load_model


class HKSNet(BaseNet):
    def __init__(self, observation_shape, num_actions, flags, device):
        super(HKSNet, self).__init__(observation_shape, num_actions, flags, device)

        options_path = flags.foc_options_path.split("-")
        configs_path = flags.foc_options_config_path.split("-")

        if len(options_path) != len(configs_path):
            print(options_path)
            print(configs_path)
            raise ValueError(
                "options_path length does not equal configs_length "
                + str(len(options_path))
                + " "
                + str(len(configs_path))
            )

        self.num_options = len(options_path)

        self.options = [
            load_model(flags.env, paths[0], paths[1], device)[0]
            for paths in zip(options_path, configs_path)
        ]

        self.pot = BaseNet(observation_shape, self.num_options, flags, device)

    def forward(self, inputs, core_state, learning=False):
        (output, core_state) = super().forward(inputs, core_state, learning)

        (pot_output, _) = self.pot.forward(inputs, core_state, learning)

        pot_sm = torch.softmax(pot_output["policy_logits"], 2)

        with torch.no_grad():
            option_sm = [
                torch.softmax(
                    self.options[i](inputs, core_state, learning)[0]["policy_logits"], 2
                )
                for i in range(len(self.options))
            ]

        weighted_teacher = (
            pot_sm[:, :, 0].unsqueeze(2).repeat(1, 1, self.num_actions) * option_sm[0]
        )

        for i in range(1, self.num_options):
            weighted_teacher += (
                pot_sm[:, :, i].unsqueeze(2).repeat(1, 1, self.num_actions)
                * option_sm[i]
            )

        return (
            dict(
                policy_logits=output["policy_logits"],
                baseline=output["baseline"],
                action=output["action"],
                chosen_option=output["action"],
                teacher_logits=weighted_teacher,  # TODO not actually logits anymore
            ),
            core_state,
        )
