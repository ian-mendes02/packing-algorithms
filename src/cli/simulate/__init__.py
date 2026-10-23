from typer import Argument, Option
from typing_extensions import Annotated


def simulate(
    algo: Annotated[
        str,
        Argument(
            help="The algorithm to use in the simulation (either 'GGA' or 'FFD').",
        ),
    ],
    size: Annotated[
        int | None,
        Option(
            help="The number of items in the cart to generate. Must be provided if 'source' is not specified.",
        ),
    ] = None,
    source: Annotated[
        str | None,
        Option(
            help="Specifies a path to load the cart from. This will skip the random cart generation step and use the provided one instead. If 'source' is specified, this option will be ignored.",
        ),
    ] = None,
    save: Annotated[
        str | None,
        Option(
            help="Specifies a path to save the generated cart to. If not specified, the cart will not be saved.",
        ),
    ] = None,
):
    from .scene import show_result_3d
    from src.factories import create_cart, generate_payload
    from src.schema import Payload
    from src.solver import Solver
    import json

    algo = algo.upper()

    if algo not in ["FFD", "GGA"]:
        raise ValueError("'algo' must be one of 'FFD', 'GGA'")

    if size == 0:
        raise ValueError("'size' must be greater than 0.")

    if source:
        with open(source, "r", encoding="utf-8") as f:
            product_data = json.load(f)
            size = sum(item["quantity"] for item in product_data)

    else:
        if size is None:
            raise ValueError(
                "'size' must be provided if 'source' is not specified.",
            )

        product_data = create_cart(size)

        if save:
            with open(save, "w", encoding="utf-8") as f:
                json.dump(product_data, f)

    print(f"Running {algo} simulation with {size} item(s)...")

    payload = generate_payload(cart_items=product_data, algo=algo)
    instance = Solver(Payload.model_validate(payload))
    instance.execute()
    show_result_3d(instance.created_parcels(), instance.unallocated())
