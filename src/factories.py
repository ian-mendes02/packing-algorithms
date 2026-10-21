from copy import copy
from random import randrange
from typing import Literal

from src.typed_dicts import Product as ProductDict, Payload as PayloadDict
from src.config import products, containers

def create_cart(size: int) -> list[ProductDict]:
    cart_items = {}

    for _ in range(size):
        j = randrange(len(products))
        target = products[j]
        sku = target["sku"]

        if sku in cart_items:
            cart_items[sku]["quantity"] += 1
        else:
            product = copy(target)
            product["quantity"] = 1
            cart_items[sku] = product

    return list(cart_items.values())


def generate_payload(
    cart_items: int | list[ProductDict],
    algo: Literal["FFD", "GGA"],
) -> PayloadDict:
    cart_items = cart_items \
        if isinstance(cart_items, list) \
        else create_cart(cart_items)

    return {
        "cart": cart_items,
        "containers": containers,
        "algo": algo,
    }
