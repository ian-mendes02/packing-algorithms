from typing import NamedTuple, TypeAlias

from src.objects.geometry import Orientation
from src.objects.packing import PackingResult
from src.config import params

from .chromosome import Chromosome

Phenotype: TypeAlias = PackingResult

_height_penalty = params.gga_height_penalty_factor

class Genotype(NamedTuple):
    priority_sequence: Chromosome[int]
    orientation_sequence: Chromosome[Orientation]


def _calculate_fitness(phenotype: Phenotype) -> float:
    sum_fitness = 0.0

    for parcel in phenotype.parcels:
        num_packages = len(parcel.packages)
        sum_z = sum(p.z + (p.height / 2.0) for p in parcel.packages)
        mean_z = sum_z / num_packages
        height_score = mean_z / parcel.height * _height_penalty
        occupation_score = parcel.occupation_ratio() * num_packages
        sum_fitness += occupation_score - height_score

    num_parcels = max(1.0, len(phenotype.parcels))

    return sum_fitness / num_parcels - len(phenotype.unallocated)


class Individual:
    genotype: Genotype
    phenotype: Phenotype
    fitness: float

    def __init__(
        self,
        genotype: Genotype,
        phenotype: Phenotype,
    ) -> None:
        self.genotype = genotype
        self.phenotype = phenotype
        self.fitness = _calculate_fitness(self.phenotype)

    def __repr__(self) -> str:
        return f"Individual({self.fitness:.2f})"

    def __eq__(self, other: Individual) -> bool:
        return self.fitness == other.fitness

    def __lt__(self, other: Individual) -> bool:
        return self.fitness < other.fitness

    def __gt__(self, other: Individual) -> bool:
        return self.fitness > other.fitness

    def __float__(self) -> float:
        return self.fitness
