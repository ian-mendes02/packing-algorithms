from dataclasses import dataclass
from typing import Sequence

from .box import Box
from .geometry import (
    Orientation,
    Point3D,
    DEFAULT_ORIENTATION,
    FRAGILE_ORIENTATIONS,
    ALL_ORIENTATIONS,
)


class Package(Box):
    valid_orientations: Sequence[Orientation]
    sku: str
    weight: float
    is_fragile: bool

    def __init__(
        self,
        dimensions: tuple[float, float, float],
        sku: str,
        weight: float,
        is_fragile: bool,
        position: Point3D | None = None,
        orientation: Orientation = DEFAULT_ORIENTATION,
    ) -> None:
        super().__init__(dimensions, position, orientation)
        self.sku = sku
        self.weight = weight
        self.is_fragile = is_fragile
        self.valid_orientations = FRAGILE_ORIENTATIONS \
            if is_fragile \
            else ALL_ORIENTATIONS

    def __repr__(self) -> str:
        return f"Package({self.sku})"


class Container(Box):
    id: str
    base_weight: float
    capacity: float

    def __init__(
        self,
        container_id: str,
        length: float,
        width: float,
        height: float,
        base_weight: float,
        capacity: float,
    ) -> None:
        super().__init__((length, width, height))
        self.id = container_id
        self.base_weight = base_weight
        self.capacity = capacity

    def __repr__(self) -> str:
        return f"Container({self.id})"


class Parcel:
    container: Container
    packages: list[Package]
    height: float

    def __init__(
        self,
        container: Container,
        packages: list[Package],
    ) -> None:
        self.container = container
        self.packages = packages
        self.height = self.container.height

    def __repr__(self) -> str:
        return (
            f"Parcel(container={self.container.id}, "
            f"packages={len(self.packages)})"
        )

    def occupation_ratio(self) -> float:
        return sum(c.volume for c in self.packages) / self.container.volume


@dataclass(frozen=True)
class PackingResult:
    parcels: list[Parcel]
    unallocated: list[Package]


class ContainerCollection:
    __containers: list[Container]
    __current_index: int
    __size: int
    __range: range

    def __init__(self, containers: list[Container]) -> None:
        self.__containers = sorted(
            containers,
            key=lambda c: c.volume,
        )
        self.__current_index = 0
        self.__size = len(self.__containers)
        self.__range = range(self.__size)

    def __repr__(self) -> str:
        return f"ContainerCollection({self.__size})"

    def next(self) -> Container | None:
        if self.__current_index + 1 < self.__size:
            self.__current_index += 1
            return self.__containers[self.__current_index]

        return None

    def best_fit(self, target_volume: float) -> Container:
        for i in self.__range:
            self.__current_index = i
            if self.__containers[i].volume >= target_volume:
                break

        return self.__containers[self.__current_index]
