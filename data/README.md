# packing-algorithms/data

This directory contains the data files used in the project, including configuration files, product catalogs, and sample input data for testing the packing algorithms.

If you wish to override the default application parameters, you may do so in a `config.json` file, which can be generated via the `generate-config` command. This documentation provides an overview of the data files and their structure.

> [!NOTE]
> Manual configuration is **not required** to run the application. 
> 
> All fields in `config.json` are optional and will be assigned default values if not provided. See the [default configuration file](default_config.json) for more information.

## Configuration

> [!IMPORTANT]
> This application is unit-agnostic, but it is recommended to use the same unit of measurement for all dimensions and weights. The default configuration uses centimeters for dimensions and grams for weights.


### Defining a product catalog

The product catalog will be sampled from to generate the carts used for benchmarking and is defined in the `products` field. 

The field can either be a path to a JSON file containing the product catalog or an array of products. 
Each product should be defined as follows:

```json
{
  "sku": "SLP",
  "name": "Light Package (S)",
  "dimensions": {
    "length": 5.0,
    "width": 5.0,
    "height": 7.5
  },
  "weight": 82.0,
  "is_fragile": false
}
```
If not provided, the product catalog will be set to a predefined one. See the [default product catalog](products.json) for more information.

> [!NOTE]
> The product catalog is not required to specify quantities for each product, as the application will generate random quantities for each product when generating carts.

### Defining containers (bins)

The container catalog will be used by both algorithms to process all input carts and is defined in the `containers` field. 

The field can either be a path to a JSON file containing the container catalog or an array of containers. Each container should be defined as follows:

```json
{
  "id": "P04",
  "dimensions": {
    "length": 16.0,
    "width": 12.0,
    "height": 4.0
  },
  "base_weight": 21.28,
  "capacity": 1500
},
```

Where `capacity` is the maximum weight the container can hold.

If not provided, the container catalog will be set to a predefined one. See the [default container catalog](containers.json) for more information.


### Execution parameters

The `params` field contains various execution parameters used by the application. Any omitted values will be set to predefined ones. See the [default execution parameters](default_config.json) for more information.

```json
{
  "params": {
    "minimum_support_ratio": 0.8,
    "gga_height_penalty_factor": 1.25,
    "gga_mutation_probability": 0.25,
    "gga_population_size": 64,
    "gga_max_iterations": 100,
    "gga_convergence_limit": 10,
    "gga_seed": null
  }
}
```

Where:

- `minimum_support_ratio` is the minimum ratio of support required for a product to be considered stable in a container;
- `gga_height_penalty_factor` penalizes GGA solutions that stack many items on top of one another;
- `gga_mutation_probability` is the probability of mutation for a GGA genotype during crossover;
- `gga_population_size` is the size of each GGA population;
- `gga_max_iterations` is the maximum number of GGA iterations;
- `gga_convergence_limit` is the number of iterations without improvement before the GGA population is considered to have converged;
- `gga_seed` is the random seed used for GGA execution.

> [!TIP]
> If `gga_seed` is set to `null`, Python will use the system time to generate a random seed each run. Setting a fixed seed will ensure reproducibility of results.

### Benchmarking parameters

The `benchmark` field can be used to configure how execution metrics are exported:

```json
{
  "benchmark": {
        "cart_sizes": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 24, 28, 32, 46, 50],
        "export": {
            "occupation_ratio": {
                "title": "Average occupation ratio per cart size by algorithm",
                "path": "./data/export/occupation-ratio.png",
                "xlabel": "Number of items in cart",
                "ylabel": "Average occupation ratio (%)"
            },
            "execution_times": {
                "title": "Average execution time per cart size by algorithm",
                "path": "./data/export/execution-times.png",
                "xlabel": "Number of items in cart",
                "ylabel": "Average execution time (ms)"
            },
            "parcel_count": {
                "title": "Average number of parcels per cart size by algorithm",
                "path": "./data/export/parcel-count.png",
                "xlabel": "Number of items in cart",
                "ylabel": "Average number of parcels"
            }
        },
        "colors": {
            "ffd": "#1f77b4",
            "gga": "#ff7f0e"
        }
    }
}
```

Each value in the `cart_sizes` array will be used to generate a random cart, which will be fed into both algorithms for comparison. 

> [!NOTE]
> Any number of values may be provided, but keep in mind that large ranges may take longer to process and be harder to visualize in a graph.