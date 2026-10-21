from random import random, getrandbits
from typing import Callable, Iterable, Self

from src.protocols import PackingAlgorithm
from src.functions import flike, randbelow, choice, shuffled
from src.objects.packing import Package, PackingResult, Container
from src.objects.geometry import Orientation, DEFAULT_ORIENTATION
from src.config import params

from .chromosome import Chromosome
from .individual import Individual, Genotype
from .population import Population
from .validator import Validator

_population_range = range(params.gga_population_size)
_mutation_probability = params.gga_mutation_probability


class Packager(PackingAlgorithm):
    __packages: list[Package]
    __containers: list[Container]
    __current_population: Population
    __validator: Validator
    __most_fit: Individual
    __best_fitness: float
    __prev_best_fitness: float
    __convergence_count: int
    __iteration_count: int
    __n: int
    __fragility_map: dict[Orientation, list[bool]]

    @classmethod
    def new(
        cls,
        containers: list[Container],
        packages: list[Package],
    ) -> Self:
        return cls(containers, packages)

    def __init__(
        self,
        containers: list[Container],
        packages: list[Package],
    ) -> None:
        self.__containers = sorted(containers, key=lambda c: c.volume)
        self.__packages = list(packages)
        self.__validator = Validator(self.__containers, self.__packages)
        self.__n = len(self.__packages)
        self.__convergence_count = 0
        self.__iteration_count = 0
        self.__fragility_map = {o: [False] * self.__n for o in Orientation}

        for i, p in enumerate(self.__packages):
            for o in p.valid_orientations:
                self.__fragility_map[o][i] = True

    def execute(self) -> PackingResult:
        if not self.__packages:
            return PackingResult([], [])

        self.__initialize()

        while self.__iteration_count < params.gga_max_iterations:
            self.__iterate()

            if self.__converged():
                break

        return self.__most_fit.phenotype

    def __converged(self) -> bool:
        if flike(self.__best_fitness, self.__prev_best_fitness):
            self.__convergence_count += 1

            if self.__convergence_count >= params.gga_convergence_limit:
                return True
        else:
            self.__convergence_count = 0

        return False

    def __initialize(self) -> None:
        self.__current_population = Population(
            self.__generate(self.__random_genotype),
        )
        self.__most_fit = self.__current_population.most_fit()
        self.__best_fitness = self.__most_fit.fitness
        self.__prev_best_fitness = self.__best_fitness
        self.__iteration_count = 0

    def __iterate(self) -> None:
        self.__current_population.merge(self.__generate(self.__offspring))
        self.__most_fit = self.__current_population.most_fit()
        self.__prev_best_fitness = self.__best_fitness
        self.__best_fitness = self.__most_fit.fitness
        self.__iteration_count += 1

    def __generate(
        self,
        fn: Callable[[], Genotype],
    ) -> Iterable[Individual]:
        genotypes = [fn() for _ in _population_range]
        phenotypes = map(self.__validator.validate, genotypes)

        return (Individual(g, p) for g, p in zip(genotypes, phenotypes))

    def __random_genotype(self) -> Genotype:
        s = Chromosome(shuffled(range(self.__n)))
        r = Chromosome(choice(self.__packages[i].valid_orientations) for i in s)

        return Genotype(s, r)

    def __offspring(self) -> Genotype:
        parent_a, parent_b = sorted(
            self.__current_population.sample(2),
            reverse=True,
        )

        s = self.__priority_crossover(
            parent_a.genotype.priority_sequence,
            parent_b.genotype.priority_sequence,
        )

        if random() < _mutation_probability:
            i, j = randbelow(self.__n), randbelow(self.__n)
            s[i], s[j] = s[j], s[i]

        r = self.__orientation_crossover(
            s,
            parent_a.genotype.orientation_sequence,
            parent_b.genotype.orientation_sequence,
        )

        if random() < _mutation_probability:
            i = randbelow(self.__n)
            r[i] = choice(self.__packages[i].valid_orientations)

        return Genotype(s, r)

    def __priority_crossover(
        self,
        a: Chromosome[int],
        b: Chromosome[int],
    ) -> Chromosome[int]:
        start, end = sorted([randbelow(self.__n), randbelow(self.__n)])
        rest = [s for i, s in enumerate(b) if i < start or i >= end]

        return Chromosome(rest[:start] + a[start:end] + rest[start:])

    def __orientation_crossover(
        self,
        sequence: Chromosome[int],
        a: Chromosome[Orientation],
        b: Chromosome[Orientation],
    ) -> Chromosome[Orientation]:
        seq = []

        for i, o_a, o_b in zip(sequence, a, b):
            opts = (o_a, o_b)
            index = getrandbits(1) # 0 or 1
            new_o = opts[index]

            if not self.__fragility_map[new_o][i]:
                # try the other orientation
                new_o = opts[not index]

                if not self.__fragility_map[new_o][i]:
                    # fallback to default
                    new_o = DEFAULT_ORIENTATION

            seq.append(new_o)

        return Chromosome(seq)