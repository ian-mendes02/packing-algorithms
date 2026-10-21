from .protocols import PackingAlgorithm
from .objects.packing import Package, Container, Parcel
from .functions import partitioned
from .schema import Payload, Product
from .adapters import ContainerAdapter, PackageAdapter
from .algorithms import FFD3DPackager, GGAPackager


class Solver:
    __payload: Payload
    __created_parcels: list[Parcel]
    __ignored: list[str]
    __max_container: Container
    __containers: list[Container]
    __sku_map: dict[str, Product]
    __num_processed: int

    def __init__(self, payload: Payload):
        self.__payload = payload
        self.__created_parcels = []
        self.__ignored = []
        self.__num_processed = 0
        self.__containers = sorted(
            map(ContainerAdapter.from_schema, payload.containers),
            key=lambda c: c.volume,
        )
        self.__max_container = self.__containers[len(self.__containers) - 1]
        self.__sku_map = {i.sku: i for i in payload.cart}

    def execute(self) -> None:
        if not self.__payload.cart:
            return

        valid, oversized = partitioned(
            [
                item
                for item in self.__payload.cart
                for _ in range(item.quantity)
            ],
            lambda p: (p.dimensions.length
                       * p.dimensions.width
                       * p.dimensions.height) <= self.__max_container.volume,
        )

        if not valid:
            return

        if oversized:
            self.__created_parcels += oversized.map(
                lambda p: Parcel(ContainerAdapter.from_product(p), []),
            )

        self.__num_processed = len(valid)
        packages = valid.map(PackageAdapter.from_schema)

        algorithm: type[PackingAlgorithm]

        match self.__payload.algo:
            case "FFD":
                algorithm = FFD3DPackager
            case "GGA":
                algorithm = GGAPackager
            case _:
                raise ValueError(
                    f"Unknown algorithm option '{self.__payload.algo}'",
                )

        result = algorithm.new(
            self.__containers,
            list(packages),
        ).execute()

        if result.unallocated:
            self.__ignored += [package.sku for package in result.unallocated]

        self.__created_parcels += result.parcels

    def num_processed(self) -> int:
        return self.__num_processed

    def num_ignored(self) -> int:
        return len(self.__ignored)

    def created_parcels(self) -> list[Parcel]:
        return self.__created_parcels

    def unallocated(self) -> list[Package]:
        return [
            PackageAdapter.from_schema(self.__sku_map[sku])
            for sku in self.__ignored
        ]
