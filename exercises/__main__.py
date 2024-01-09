import click
from .composite import run_example as composite
from .strategy import run_example as strategy
from .command import run_example as command


@click.group()
def cli():
    pass


cli.command(name="composite", help="Composite exercise example")(composite)
cli.command(name="strategy", help="Strategy exercise example")(strategy)
cli.command(name="command", help="Command exercise example")(command)


if __name__ == "__main__":
    cli()
