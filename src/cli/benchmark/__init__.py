from typer import Argument
from typing_extensions import Annotated


def benchmark(
    rounds: Annotated[int, Argument(
        help="The number of rounds to run.",
    )],
):
    from .functions import run_benchmark
    from src.config import benchmark as config
    from src.factories import create_cart
    import src.cli.benchmark.plotting as plt

    if not config.cart_sizes:
        raise Exception("No cart sizes provided.")

    cart_sizes: list[int] = sorted(config.cart_sizes)
    dataset = [create_cart(size) for size in cart_sizes]
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
