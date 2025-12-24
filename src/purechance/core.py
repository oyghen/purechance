__all__ = ("Seed", "coinflip", "draw", "get_rng", "integers", "shuffle")

import random
from collections.abc import Iterator
from typing import TypeAlias, TypeVar

T = TypeVar("T")
Seed: TypeAlias = int | random.Random | None


def coinflip(bias: float, seed: Seed = None) -> bool:
    """Return outcome of a simulated random coin flip with a specified bias."""
    if not (0 <= bias <= 1):
        raise ValueError(f"invalid {bias=!r}; expected 0 <= bias <= 1")
    rng = get_rng(seed)
    return rng.random() < bias


def draw(items: list[T], replace: bool, size: int, seed: Seed = None) -> list[T]:
    """Return a new list of items randomly drawn from the input sequence."""
    rng = get_rng(seed)
    if size < 0:
        raise ValueError(f"invalid {size=!r}; expected >= 0")
    if len(items) == 0 or size == 0:
        return []
    return rng.choices(items, k=size) if replace else rng.sample(items, k=size)


def get_rng(seed: Seed = None) -> random.Random:
    """Return a random.Random instance from the given seed."""
    if isinstance(seed, random.Random):
        return seed
    elif seed is None or isinstance(seed, int):
        return random.Random(seed)
    else:
        raise ValueError(f"invalid {seed=!r}")


def integers(size: int, lower: int, upper: int, seed: Seed = None) -> Iterator[int]:
    """Return random integers between lower (included) and upper (excluded) endpoint."""
    rng = get_rng(seed)
    return (rng.randrange(lower, upper) for _ in range(size))


def shuffle(items: list[T], seed: Seed = None) -> list[T]:
    """Return a randomly shuffled copy of the input sequence."""
    return draw(items, replace=False, size=len(items), seed=seed)
