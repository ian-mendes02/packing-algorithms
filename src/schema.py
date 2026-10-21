from typing import Annotated, Literal
from pydantic import (
    BaseModel,
    PositiveFloat,
    PositiveInt,
    StrictBool,
    StringConstraints,
    field_validator,
)


class Dimensions(BaseModel):
    length: PositiveFloat
    width: PositiveFloat
    height: PositiveFloat


class Container(BaseModel):
    id: str
    dimensions: Dimensions
    base_weight: PositiveFloat
    capacity: PositiveFloat


class Product(BaseModel):
    sku: str
    name: str
    dimensions: Dimensions
    weight: PositiveFloat
    quantity: PositiveInt
    is_fragile: StrictBool


class Payload(BaseModel):
    containers: list[Container]
    cart: list[Product]
    algo: Annotated[Literal["FFD", "GGA"], StringConstraints(
        to_upper=True,
        strip_whitespace=True,
    )]

    @classmethod
    @field_validator("algo", mode="after")
    def validate_algo(cls, value: str):
        if value not in ["GGA", "FFD"]:
            raise ValueError(
                f"'algo' must be one of {", ".join(["GGA", "FFD"])}",
            )
        return value
