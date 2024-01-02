import click
from .composite import run_example as composite


@click.group()
def cli():
    pass


cli.command(name="composite", help="Composite example")(composite)


if __name__ == "__main__":
    cli()
