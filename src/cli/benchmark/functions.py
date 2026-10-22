from threading import Thread
from time import sleep

from src.objects.timer import Timer
from src.typed_dicts import (
    Payload as PayloadDict,
    Product as ProductDict,
)
from src.schema import Payload as PayloadSchema
from src.solver import Solver
from src.config import containers
from sys import stdout

from .objects import ExecutionReport, BenchmarkMetrics


class _ProgressLogger(Thread):
    def __init__(self, total_iterations: int) -> None:
        super().__init__()
        self.current_iteration = 0
        self.__total_iterations = total_iterations
        self.__stop = False

    def stop(self):
        self.__stop = True

    def run(self):
        frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0

        while not self.__stop:
            i = (i + 1) % 10  # len(frames)
            progress = 100 * (self.current_iteration / self.__total_iterations)
            filled_length = int(100 * self.current_iteration / self.__total_iterations)
            bar = "█" * filled_length + "-" * (100 - filled_length)

            stdout.write(
                f"\r{frames[i]} Progress: |{bar}| {progress:.2f}% "
                f"({self.current_iteration + 1}/{self.__total_iterations} iterations)",
            )
            stdout.flush()
            sleep(0.1)

        stdout.write("\n\r")


def _task(payload: PayloadDict) -> ExecutionReport:
    pld = PayloadSchema.model_validate(payload)
    instance = Solver(pld)
    timer = Timer()

    timer.start()
    instance.execute()
    timer.stop()

    created_parcels = instance.created_parcels()
    num_parcels = len(created_parcels)
    avg_occupation_ratio = sum(
        (b.occupation_ratio() for b in created_parcels),
    ) / num_parcels

    return ExecutionReport(
        num_parcels=num_parcels,
        avg_occupation_ratio=avg_occupation_ratio,
        execution_time=timer.elapsed(),
        num_ignored=instance.num_ignored(),
    )


def run_benchmark(
    dataset: list[list[ProductDict]],
    rounds: int,
) -> list[BenchmarkMetrics]:
    dataset *= rounds
    sample_count = len(dataset)
    total_iterations = sample_count * 2
    logger = _ProgressLogger(total_iterations)
    sample_sizes = [
        sum(item["quantity"] for item in items)
        for items in dataset
    ]

    ffd_payloads: list[PayloadDict] = [{
        "cart": cart,
        "containers": containers,
        "algo": "FFD",
    } for cart in dataset]

    gga_payloads: list[PayloadDict] = [{
        "cart": cart,
        "containers": containers,
        "algo": "GGA",
    } for cart in dataset]

    results = {
        size: BenchmarkMetrics(
            input_size=size,
            ffd_results=[],
            gga_results=[],
        )
        for size in sample_sizes
    }

    print(f"Running benchmark with {sample_count} cart samples...")

    # warmup
    _task(ffd_payloads[0])
    _task(gga_payloads[0])

    logger.start()

    try:
        for size, payload in zip(sample_sizes, ffd_payloads):
            results[size].ffd_results.append(_task(payload))
            logger.current_iteration += 1

        for size, payload in zip(sample_sizes, gga_payloads):
            results[size].gga_results.append(_task(payload))
            logger.current_iteration += 1

        logger.stop()
        logger.join()

    except KeyboardInterrupt as e:
        logger.stop()
        logger.join()
        raise e

    return sorted(results.values(), key=lambda x: x.input_size)
