from typing import Protocol, Self

from .objects.packing import Package, PackingResult, Container


class PackingAlgorithm(Protocol):
    @classmethod
    def new(cls, containers: list[Container], packages: list[Package]) -> Self:
        ...

    def execute(self) -> PackingResult:
        ...
