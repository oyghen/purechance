import typer
from rich.console import Console

import purechance

console = Console()
app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def version(
    show: bool = typer.Option(
        False, "--version", "-v", help="Show app version and exit."
    ),
) -> None:
    if show:
        typer.echo(f"{purechance.__name__} {purechance.__version__}")
        raise typer.Exit()


def main() -> None:
    """Canonical entry point for CLI execution."""
    app()
