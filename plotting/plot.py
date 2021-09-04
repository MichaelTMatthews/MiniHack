import wandb
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.ticker import FuncFormatter


def millions(x, pos):
    "The two args are the value and tick position"
    return "%1.0fM" % (x * 1e-6)


def get_run(runs, name):
    for run in runs:
        if run.name == name:
            return run

    print("No run with name", name)


def smooth(x, y, smooth_width=200):

    span = x[-1] - x[0]
    span /= smooth_width
    new_y = np.zeros(len(y))

    for i in range(len(x)):
        normalised_x = (x - x[i]) / span
        coeffs = norm.pdf(normalised_x)
        coeffs /= np.sum(coeffs)
        prod = coeffs * y

        new_y[i] = np.sum(prod)

    return new_y


def plot_run(run, label=""):
    h = run.history()
    x = h["step"].to_numpy()
    y = h["success_rate"].to_numpy()

    # plt.plot(x, y, label=label)

    y = smooth(x, y)

    plt.plot(x, y, label=label)


def plot_comparison(runs, names):
    # Vanilla
    # IC
    # FOC
    # KS

    models = ["Vanilla", "Interleaved Curriculum", "Options Framework", "Kickstarting"]

    plt.style.use("seaborn")

    formatter = FuncFormatter(millions)
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(formatter)

    for name, model_name in zip(names, models):
        run = get_run(runs, name)
        plot_run(run, label=model_name)

    plt.legend()
    plt.xlabel("Timesteps")
    plt.ylabel("Success Rate")
    plt.title("Battle")

    plt.show()


SIMPLE_SEQ = {
    "names": ["rich-silence-32", "azure-yogurt-68", "apricot-lake-60", "easy-wind-93"]
}


if __name__ == "__main__":
    wandb.login
    api = wandb.Api()
    runs = api.runs("michaelmatthews/minihack_results")

    env = SIMPLE_SEQ
    run_names = env["names"]

    plot_comparison(runs, run_names)
