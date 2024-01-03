import click
from .composite import run_example as composite
from .strategy import run_example as strategy


@click.group()
def cli():
    pass


cli.command(name="composite", help="Composite exercise example")(composite)
cli.command(name="strategy", help="Strategy exercise example")(strategy)


if __name__ == "__main__":
    cli()
