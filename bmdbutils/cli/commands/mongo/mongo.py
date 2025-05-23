"""
$ bmdbutils mongo
"""
import configparser
import os

import appdirs
import click

from bmdbutils.biomodelos.mongo import Mongo
from .setup import setup
from .upload import upload
from .validate import validate


@click.group(
    short_help="Operaciones relacionadas con base de datos MongoDB de BioModelos.",
)
@click.pass_context
def mongo(ctx):
    if ctx.invoked_subcommand != "setup":
        config = configparser.ConfigParser()
        config.read(
            os.path.join(appdirs.user_config_dir("bmdbutils"), "mongo")
        )
        if not "MONGODB" in config.sections():
            click.secho(
                "La conexión a la base de datos de MongoDB no ha sido configurada correctamente.",
                fg="red",
                blink=True,
            )
            click.secho(
                "Primero ejecute 'bmdbutils mongo setup'",
                fg="yellow",
                blink=True,
                bold=True,
            )
            ctx.exit(0)
        else:
            ctx.obj = Mongo(
                mongo_url=config["MONGODB"]["url"],
                mongo_user=config["MONGODB"]["username"],
                mongo_pass=config["MONGODB"]["password"],
                mongo_db=config["MONGODB"]["db"],
            )


mongo.add_command(setup)
mongo.add_command(upload)
mongo.add_command(validate)
