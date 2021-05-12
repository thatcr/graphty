"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Grafty."""


if __name__ == "__main__":
    main(prog_name="grafty")  # pragma: no cover
