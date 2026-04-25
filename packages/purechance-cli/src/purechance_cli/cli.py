from collections import Counter
from typing import Annotated

import purechance
import typer
from rich.console import Console

console = Console()
app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
) -> None:
    pkg_name = purechance.__name__
    pkg_version = typer.style(purechance.__version__, fg=typer.colors.CYAN)

    if version:
        typer.echo(f"{pkg_name} {pkg_version}")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.echo(f"{pkg_name} {pkg_version} ready. See --help for usage.")
        raise typer.Exit()


@app.command()
def coinflips(
    size: int = typer.Argument(1, help="Number of coin flips."),
    bias: float = typer.Option(0.5, "--bias", help="Chance of True."),
    seed: int | None = typer.Option(None, "--seed", help="RNG seed."),
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
    seed: int | None = typer.Option(None, "--seed", help="RNG seed."),
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
    seed: int | None = typer.Option(None, "--seed", help="RNG seed."),
) -> None:
    """Show randomly selected items from the input sequence."""
    rng = purechance.get_rng(seed)
    picked = purechance.draw(items, replace, size, rng)
    console.print(picked)


@app.command()
def shuffle(
    items: Annotated[list[str], typer.Argument(help="Input items.")],
    seed: int | None = typer.Option(None, "--seed", help="RNG seed."),
) -> None:
    """Show the input sequence in a randomly shuffled order."""
    rng = purechance.get_rng(seed)
    shuffled = purechance.shuffle(items, rng)
    console.print(shuffled)
