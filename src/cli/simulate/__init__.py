from typer import Argument
from typing_extensions import Annotated


def simulate(
    algo: Annotated[
        str,
        Argument(
            help="The algorithm to use in the simulation (either 'GGA' or 'FFD').",
        ),
    ],
    cart_size: Annotated[
        int,
        Argument(help="The number of items in the cart to simulate."),
    ]
):
    from .scene import show_result_3d
    from src.factories import create_cart, generate_payload
    from src.schema import Payload
    from src.solver import Solver

    algo = algo.upper()

    if algo not in ["FFD", "GGA"]:
        raise ValueError("'algo' must be one of 'FFD', 'GGA'")

    print(f"Running {algo} simulation with {cart_size} item(s)...")

    product_data = create_cart(cart_size)
    payload = generate_payload(cart_items=product_data, algo=algo)
    instance = Solver(Payload.model_validate(payload))
    instance.execute()
    show_result_3d(instance.created_parcels(), instance.unallocated())
