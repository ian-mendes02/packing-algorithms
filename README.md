# packing-algorithms

## About

This project is a comparative study on well-known solutions to the 3D Bin Packing Problem (3D-BPP) and how they perform in the context of last-mile logistics.

Two algorithms were implemented:

- A genetic grouping algorithm (GGA);
- A 3D first-fit decreasing algorithm (3D-FFD) with extreme point heuristics.

## Installation

### Setup

> [!IMPORTANT]
> Python >= 3.14 is required to run this application.

To run the application, first set up a virtual environment. Open your terminal in the target folder and run:

- **macOS/Unix:** `python3 -m venv .venv`
- **Windows**: `python -m venv .venv` or `py -m venv .venv`

Before installing any packages, make sure to activate the environment:

- **macOS/Unix:** `source .venv/bin/activate`
- **Windows**: `.venv\Scripts\Activate.ps1`

To deactivate it, run:

```bash
deactivate
```

### Installing dependencies

To install the required dependencies, first make sure the virtual environment is active, then run:

```bash
python -m pip install .
```

## Configuration

The `config.json` file can be used to override the application's default execution parameters and should live in the project's root directory.

A `config.json` file is not provided by default. If you wish to customize the application parameters, you may create your own `config.json` file, or generate one via the `generate-config` command.

> [!NOTE]
> All fields are optional and will be assigned default values if not provided. See the [default configuration file](data/default_config.json) for more information.

### Defining a product catalog

The `products` field can either be a path to a JSON file containing the product catalog or an array of products. Each product should be defined as follows:

```json
{
  "sku": <string>,
  "name": <string>,
  "dimensions": {
    "width": <float>,
    "height": <float>,
    "depth": <float>
  },
  "weight": <float>,
  "is_fragile": <boolean>
}
```

> [!NOTE]
> If not provided, the product catalog will be set to a predefined one. See the [default product catalog](data/products.json) for more information.

### Defining containers (bins)

The `containers` field can either be a path to a JSON file containing the container catalog or an array of containers. Each container should be defined as follows:

```json
{
  "id": <string>,
  "dimensions": {
    "width": <float>,
    "height": <float>,
    "depth": <float>
  },
  "base_weight": <float>,
  "capacity": <float>
}
```

Where `capacity` is the maximum weight the container can hold.

> [!NOTE]
> If not provided, the container catalog will be set to a predefined one. See the [default container catalog](data/containers.json) for more information.

### Execution parameters

The `params` field in the configuration file allows you to specify various execution parameters.

```json
{
  "minimum_support_ratio": <float>,
  "gga_height_penalty_factor": <float>,
  "gga_mutation_probability": <float>,
  "gga_population_size": <int>,
  "gga_max_iterations": <int>,
  "gga_convergence_limit": <int>
}
```

> [!NOTE]
> If not provided, the execution parameters will be set to predefined values. See the [default execution parameters](data/default_config.json) for more information.

Where:

- `minimum_support_ratio` is the minimum ratio of support required for a product to be considered stable in a container;
- `gga_height_penalty_factor` penalizes GGA solutions that stack many items on top of one another;
- `gga_mutation_probability` is the probability of mutation for a GGA genotype during crossover;
- `gga_population_size` is the size of each GGA population;
- `gga_max_iterations` is the maximum number of GGA iterations;
- `gga_convergence_limit` is the number of iterations without improvement before the GGA population is considered to have converged.

### Benchmarking parameters

The `benchmark` field can be used to configure how execution metrics are exported:

```json
{
  "benchmark": {
    "cart_sizes": [<int>, ...],
    "colors": {
      "ffd": <color>,
      "gga": <color>
    },
    "export": {
      <graph_id>: {
        "title": <string>,
        "xlabel": <string>,
        "ylabel": <string>,
        "filename": <string>
      },
      ...
    }
  }
}
```

- `cart_sizes` is an array of cart sizes; each will be used to generate a random cart, which will be fed into both algorithms for comparison. Any number of values may be provided, but keep in mind that large ranges may take longer to process and be harder to visualize in a graph;

- `colors` defines the hex codes used to identify each algorithm in a graph;

- `<graph_id>` is the identifier of the graph to be exported. The available options are:
    - `occupation_ratio` is the average density per solution per cart size by algorithm;
    - `execution_times` is the average execution time per cart size by algorithm;
    - `parcel_count` is the average number of parcels per solution per cart size by algorithm.

## Usage

### Running a Simulation

The `simulate` command will run a simulation of the selected algorithm using the provided number of cart items. The execution result will be displayed interactively using `pyvista`.

```bash
python . simulate {algo} {cart_size}
```

- `algo` specifies the selected algorithm:
    - `ffd` will select the first-fit decreasing algorithm;
    - `gga` will select the genetic grouping algorithm.
- `cart_size` specifies the number of cart items. The cart will be populated randomly from the configured product catalog.


### Benchmarking

The `benchmark` command will run a benchmark of both algorithms using the configured range of cart sizes, for the provided number of rounds. The execution graphs will be exported via `matplotlib`.

```bash
python . benchmark {rounds=1}
```

> [!TIP]
> Due to the randomness of the genetic algorithm, it is recommended to run 5 or more rounds to obtain a more accurate comparison between the two algorithms.

### Generating a configuration file

The `generate-config` command will generate a `config.json` with default values in the project's root directory:

```bash
python . generate-config
```