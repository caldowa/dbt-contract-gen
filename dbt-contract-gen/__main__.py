# __main__.py

import click

from . import commands


@click.group()
def cli():
    pass


cli.add_command(commands.extract)
