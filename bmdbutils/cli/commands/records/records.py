"""
$ bmdbutils records
"""

import os
import click

from bmdbutils.biomodelos.mongo import Mongo
from bmdbutils.biomodelos.config import load_config
from .upload import upload
from .validate import validate


@click.group(
    help=""" Comando relacionado con la base de datos MongoDB de BioModelos.""",
    short_help="Operaciones relacionadas con base de datos MongoDB de BioModelos.",
)
@click.pass_context
def records(ctx):
    if ctx.invoked_subcommand in ["upload", "validate"]:
        config = load_config()
        if not "MONGODB" in config.sections():
            click.secho(
                "La conexión a la base de datos de MongoDB no ha sido configurada correctamente.",
                fg="red",
            )
            click.secho(
                "Primero ejecute 'bmdbutils setup mongo'",
                fg="yellow",
                bold=True,
            )
            ctx.exit(0)
        else:
            ctx.obj = Mongo(
                mongo_url=config["MONGODB"]["url"],
                mongo_user=config["MONGODB"]["username"],
                mongo_pass=config["MONGODB"]["password"],
                mongo_db=config["MONGODB"]["database"],
            )


records.add_command(upload)
records.add_command(validate)
