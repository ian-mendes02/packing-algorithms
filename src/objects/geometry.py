from enum import IntEnum
from typing import Sequence, NamedTuple, Callable

type Vec3D = tuple[float, float, float]


class Orientation(IntEnum):
    """
    An enumeration representing the six possible orientations of a rectangular box in 3D space, based on the order of its length (L), width (W), and height (H) dimensions.
    """
    LWH = 0
    LHW = 1
    WLH = 2
    WHL = 3
    HLW = 4
    HWL = 5


DEFAULT_ORIENTATION: Orientation = Orientation.LWH

ALL_ORIENTATIONS: Sequence[Orientation] = (
    Orientation.LWH,
    Orientation.LHW,
    Orientation.WLH,
    Orientation.WHL,
    Orientation.HLW,
    Orientation.HWL,
)

FRAGILE_ORIENTATIONS: Sequence[Orientation] = (
    Orientation.LWH,
    Orientation.WLH,
)


def _lwh(l: float, w: float, h: float) -> Vec3D:
    return l, w, h


def _hlw(l: float, w: float, h: float) -> Vec3D:
    return h, l, w


def _wlh(l: float, w: float, h: float) -> Vec3D:
    return w, l, h


def _whl(l: float, w: float, h: float) -> Vec3D:
    return w, h, l


def _lhw(l: float, w: float, h: float) -> Vec3D:
    return l, h, w


def _hwl(l: float, w: float, h: float) -> Vec3D:
    return h, w, l


_transpose: dict[Orientation, Callable[[float, float, float], Vec3D]] = {
    Orientation.LWH: _lwh,
    Orientation.LHW: _lhw,
    Orientation.WLH: _wlh,
    Orientation.WHL: _whl,
    Orientation.HLW: _hlw,
    Orientation.HWL: _hwl,
}


class Dimensions(NamedTuple):
    length: float
    width: float
    height: float

    def __repr__(self) -> str:
        return f"Dimensions({self.length}, {self.width}, {self.height})"

    def transposed_to(self, orientation: Orientation) -> Dimensions:
        return Dimensions(
            *_transpose[orientation](
                self.length,
                self.width,
                self.height,
            ),
        )


class Point3D(NamedTuple):
    x: float
    y: float
    z: float

    def __copy__(self) -> Point3D:
        return Point3D(self.x, self.y, self.z)

    def __eq__(self, other: Point3D) -> bool:
        return not (
            self.x != other.x
            or self.y != other.y
            or self.z != other.z
        )

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f"Point3D({self.x}, {self.y}, {self.z})"
