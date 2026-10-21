from dataclasses import dataclass


@dataclass
class ExecutionReport:
    num_parcels: int
    avg_occupation_ratio: float
    execution_time: float
    num_ignored: int


@dataclass
class BenchmarkMetrics:
    input_size: int
    ffd_results: list[ExecutionReport]
    gga_results: list[ExecutionReport]
