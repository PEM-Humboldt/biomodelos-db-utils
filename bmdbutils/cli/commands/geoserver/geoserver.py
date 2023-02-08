"""
$ bmdbutils geoserver
"""
import configparser
import os

import appdirs
import click

from bmdbutils.biomodelos.geoserver import Geoserver
from .setup import setup
from .upsert import upsert


@click.group(
    short_help="Operaciones relacionadas con GeoServer",
)
@click.pass_context
def geoserver(ctx):
    if ctx.invoked_subcommand != "setup":
        config = configparser.ConfigParser()
        config.read(os.path.join(appdirs.user_config_dir("bmdbutils"), "geoserver"))
        if (
            len(config.sections()) <= 0
            or not "LOCATION" in config.sections()
            or not "CREDENTIALS" in config.sections()
        ):
            click.echo(
                "Geoserver no ha sido configurado o la configuración es erronea. "
                "Primero ejecute 'bmdbutils geoserver setup'"
            )
            ctx.exit(0)

        ctx.obj = Geoserver(
            config["LOCATION"]["url"],
            config["CREDENTIALS"]["username"],
            config["CREDENTIALS"]["password"],
        )


geoserver.add_command(setup)
geoserver.add_command(upsert)
