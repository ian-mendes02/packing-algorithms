from typing import TYPE_CHECKING
from os import path, getcwd
from json import loads
from data import ROOT as DATA_ROOT

from dataclasses import dataclass

if TYPE_CHECKING:
    from typed_dicts import (
        Product as ProductDict,
        Container as ContainerDict,
    )


@dataclass(frozen=True)
class _ExportConfig:
    title: str
    path: str
    xlabel: str
    ylabel: str


@dataclass(frozen=True)
class _BenchmarkConfig:
    cart_sizes: list[int]
    export: dict[str, _ExportConfig]
    colors: dict[str, str]

    @staticmethod
    def new(data: dict) -> _BenchmarkConfig:
        return _BenchmarkConfig(
            cart_sizes=data.get("cart_sizes", []),
            export={
                key: _ExportConfig(**value)
                for key, value in data["export"].items()
            },
            colors=data.get("colors", {}),
        )


@dataclass(frozen=True)
class _ExecutionParams:
    minimum_support_ratio: float = 0.8
    gga_height_penalty_factor: float = 1.15
    gga_mutation_probability: float = 0.25
    gga_population_size: int = 64
    gga_max_iterations: int = 100
    gga_convergence_limit: int = 10
    gga_seed: int | None = None


@dataclass(frozen=True)
class _Config:
    products: list["ProductDict"]
    containers: list["ContainerDict"]
    params: _ExecutionParams
    benchmark: _BenchmarkConfig


def _load(target):
    if type(target) is str:
        with open(target, "r", encoding="utf-8") as f:
            data = loads(f.read())
        return data

    return target


def _fill_missing(a: dict, b: dict) -> dict:
    for key, value in b.items():
        if key not in a:
            a[key] = value
        elif isinstance(value, dict) and isinstance(a[key], dict):
            a[key] = _fill_missing(a[key], value)

    return a


def _load_config() -> _Config:
    configpath = path.join(getcwd(), "config.json")

    with open(
        path.join(DATA_ROOT, "default_config.json"),
        "r",
        encoding="utf-8",
    ) as f:
        default_config: dict = loads(f.read())

    if path.exists(configpath):
        with open(configpath, "r", encoding="utf-8") as f:
            data = loads(f.read())
            config = _fill_missing(data, default_config)

    else:
        config = default_config

    return _Config(
        products=_load(config["products"]),
        containers=_load(config["containers"]),
        params=_ExecutionParams(**config["params"]),
        benchmark=_BenchmarkConfig.new(config["benchmark"]),
    )


_config = _load_config()
products = _config.products
containers = _config.containers
params = _config.params
benchmark = _config.benchmark
