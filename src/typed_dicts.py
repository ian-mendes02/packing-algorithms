from typing import TypedDict, Literal


class Dimensions(TypedDict):
    length: float
    width: float
    height: float


class Container(TypedDict):
    id: str
    dimensions: Dimensions
    base_weight: float
    capacity: float


class Product(TypedDict):
    sku: str
    name: str
    dimensions: Dimensions
    weight: float
    quantity: int
    is_fragile: bool


class Payload(TypedDict):
    cart: list[Product]
    containers: list[Container]
    algo: Literal["FFD", "GGA"]