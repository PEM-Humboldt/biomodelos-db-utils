"""
$ bmdbutils geoserver
"""
import configparser
import os

import appdirs
import click

from .setup import setup
from .upsert import upsert

from bmdbutils.biomodelos.geoserver import Geoserver


@click.group(
    short_help="Operations related with Geoserver",
)
@click.pass_context
def geoserver(ctx):
    config = configparser.ConfigParser()
    config.read(os.path.join(appdirs.user_config_dir("bmdbutils"), "geoserver"))
    ctx.obj = Geoserver(
        config["LOCATION"]["url"],
        config["CREDENTIALS"]["username"],
        config["CREDENTIALS"]["password"],
    )


geoserver.add_command(setup)
