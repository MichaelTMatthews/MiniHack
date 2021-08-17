from nle.agent.polybeast.models.base import BaseNet
from nle.agent.polybeast.skill_transfer.skill_transfer import load_model


class KSNet(BaseNet):
    def __init__(self, observation_shape, num_actions, flags, device):
        super(KSNet, self).__init__(observation_shape, num_actions, flags, device)

        self.teacher = load_model(
            flags.env, flags.teacher_path, flags.teacher_config_path, device
        )[0]

    def forward(self, inputs, core_state, learning=False):
        (output, core_state) = super().forward(inputs, core_state, learning)
        (teacher_output, _) = self.teacher.forward(inputs, core_state, learning)

        return (
            dict(
                policy_logits=output["policy_logits"],
                baseline=output["baseline"],
                action=output["action"],
                chosen_option=output["action"],
                teacher_logits=teacher_output["policy_logits"],
            ),
            core_state,
        )
