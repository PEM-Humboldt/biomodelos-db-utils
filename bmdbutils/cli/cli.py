"""
bmdbutils CLI entry point.
"""
import configparser
import os

import appdirs
import click

from bmdbutils.biomodelos.biomodelos import Biomodelos
from .commands.geoserver.geoserver import geoserver
from .commands.setup import setup
from .commands.upload import upload


@click.group()
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand != "setup":
        config = configparser.ConfigParser()
        config.read(os.path.join(appdirs.user_config_dir("bmdbutils"), "biomodelos"))
        if len(config.sections()) <= 0 or not "API" in config.sections():
            click.echo(
                "BioModelos is misconfigured or hasn't been configured yet. "
                "You must execute 'bmdbutils setup'"
            )
            return

        ctx.obj = Biomodelos(config["API"]["url"])


main.add_command(setup)
main.add_command(upload)
main.add_command(geoserver)
