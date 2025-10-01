"""
$ bmdbutils stats
"""
import configparser
import os

import appdirs
import click

from bmdbutils.biomodelos.biomodelos import Biomodelos
from bmdbutils.biomodelos.mongo import Mongo
from .users import users
from .downloads import downloads
from .groups import groups
from .models import models


@click.group(
    help=""" Comando para realizar consultas SQL y NoSQL relacionadas con estadísticas de uso de BioModelos.""",
    short_help="Operaciones relacionadas con bases de datos de BioModelos.",
)
@click.pass_context
def stats(ctx):
    if ctx.invoked_subcommand == "models":
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
    if ctx.invoked_subcommand in ["users", "downloads", "groups"]:
        config = configparser.ConfigParser()
        config.read(
            os.path.join(appdirs.user_config_dir("bmdbutils"), "biomodelos")
        )
        if not "POSTGRESDB" in config.sections():
            click.secho(
                "La conexión a la base de datos de Postgres no ha sido configurada correctamente.",
                fg="red",
                blink=True,
            )
            click.secho(
                "Primero ejecute 'bmdbutils setup'",
                fg="yellow",
                blink=True,
                bold=True,
            )
            ctx.exit(0)
        else:
            ctx.obj = Biomodelos(
                pg_url=config["POSTGRESDB"]["url"],
                pg_user=config["POSTGRESDB"]["username"],
                pg_pass=config["POSTGRESDB"]["password"],
            )


stats.add_command(users)
stats.add_command(groups)
stats.add_command(downloads)
stats.add_command(models)
