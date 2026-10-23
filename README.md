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

> [!NOTE]
> Though manual configuration is not required to run the application, you may override the default execution parameters via a `config.json` file. 
> 
> For more information on how to configure the application parameters, see [the configuration guide](data/README.md).


## Usage

### Running a Simulation

The `simulate` command will run a simulation of the selected algorithm using the provided number of cart items. The execution result will be displayed interactively using `pyvista`.

```bash
python . simulate [OPTIONS] {algo}
```

For more information, run the command with the `--help` option:

```bash
python . simulate --help
```


### Benchmarking

The `benchmark` command will run a benchmark of both algorithms using the configured range of cart sizes, for the provided number of rounds. The execution graphs will be exported via `matplotlib`.

```bash
python . benchmark [OPTIONS] {rounds=1}
```

For more information, run the command with the `--help` option:


```bash
python . benchmark --help
```

> [!TIP]
> Due to the randomness of the genetic algorithm, it is recommended to run 5 or more rounds to obtain a more accurate comparison between the two algorithms.

> [!IMPORTANT]
> The genetic algorithm is non-deterministic, meaning that the results may vary between runs. To ensure reproducibility, you can define a random seed in the configuration file.
>
> Aditionally, the genetic algorithm is known to be *very slow*, especially for larger cart sizes. Expect longer execution times when running the benchmark with larger cart sizes.


### Generating a configuration file

The `generate-config` command will generate a `config.json` with default values in the project's root directory:

```bash
python . generate-config
```