from typer import Argument, Option
from typing_extensions import Annotated


def benchmark(
    rounds: Annotated[
        int,
        Argument(
            help="The number of rounds to run.",
        )],
    save: Annotated[
        str | None,
        Option(
            help="Specifies a path to save the carts used for benchmarking. This can be useful if you want to analyze the data later or use it for further processing. If not provided, the dataset will not be saved.",
        )] = None,
    source: Annotated[
        str | None,
        Option(
            help="Specifies a path to load a set of carts from. This will skip the random cart generation step and use the provided set instead. If not provided, new carts will be generated randomly based on the configured array of cart sizes.",
        )] = None,
):
    from .functions import run_benchmark
    from src.config import benchmark as config
    from src.factories import create_cart
    import src.cli.benchmark.plotting as plt
    import json

    if not config.cart_sizes:
        raise Exception("No cart sizes provided.")

    if source:
        with open(source, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    else:
        cart_sizes: list[int] = sorted(config.cart_sizes)
        dataset = [create_cart(size) for size in cart_sizes]

    if save:
        with open(save, "w", encoding="utf-8") as f:
            json.dump(dataset, f)

    computed_metrics = run_benchmark(dataset, rounds)

    print("Exporting execution results...")

    plt.source(computed_metrics)

    print("Plotting occupation ratio graph...")
    plt.plot_occupation_ratio_graph()

    print("Plotting execution times graph...")
    plt.plot_execution_times_graph()

    print("Plotting parcel count graph...")
    plt.plot_parcel_count_graph()

    print("Done.")
