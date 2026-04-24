from collections import Counter
from typing import Annotated

import purechance
import typer
from rich.console import Console

console = Console()
app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def version(
    show: bool = typer.Option(
        False, "--version", "-V", help="Show app version and exit."
    ),
) -> None:
    if show:
        typer.echo(f"{purechance.__name__} {purechance.__version__}")
        raise typer.Exit()


@app.command()
def coinflips(
    size: int = typer.Argument(1, help="Number of coin flips."),
    bias: float = 0.5,
    seed: int | None = typer.Option(
        None, "--seed", help="Seed for the random number generator."
    ),
) -> None:
    """Show the outcomes of random coin flips."""
    rng = purechance.get_rng(seed)
    result = [purechance.coinflip(bias, rng) for _ in range(size)]
    if size > 1:
        console.print(Counter(result))
    console.print(result)


@app.command()
def integers(
    size: int = typer.Argument(1, help="Number of random integers to sample."),
    lower: int = typer.Option(0, help="Lower bound (inclusive)."),
    upper: int = typer.Option(
        purechance.signed_max(32), help="Upper bound (exclusive)."
    ),
    seed: int | None = typer.Option(
        None, "--seed", help="Seed for the random number generator."
    ),
) -> None:
    """Show uniformly sampled random integers."""
    rng = purechance.get_rng(seed)
    values = list(purechance.integers(size, lower, upper, rng))
    console.print(values)


@app.command()
def pick(
    items: Annotated[list[str], typer.Argument(help="Input items.")],
    replace: bool = typer.Option(True, help="Sample with replacement."),
    size: int = typer.Option(1, help="Number of items to pick."),
    seed: int | None = typer.Option(
        None, "--seed", help="Seed for the random number generator."
    ),
) -> None:
    """Show randomly selected items from the input sequence."""
    rng = purechance.get_rng(seed)
    picked = purechance.draw(items, replace, size, rng)
    console.print(picked)


@app.command()
def shuffle(
    items: Annotated[list[str], typer.Argument(help="Input items.")],
    seed: int | None = typer.Option(
        None, "--seed", help="Seed for the random number generator."
    ),
) -> None:
    """Show the input sequence in a randomly shuffled order."""
    rng = purechance.get_rng(seed)
    shuffled = purechance.shuffle(items, rng)
    console.print(shuffled)


def main() -> None:
    """Canonical entry point for CLI execution."""
    app()
