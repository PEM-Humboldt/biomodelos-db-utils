"""
$ bmdbutils stats
"""
import configparser
import os

import appdirs
import click

from bmdbutils.biomodelos.biomodelos import Biomodelos
from bmdbutils.biomodelos.mongo import Mongo
from bmdbutils.biomodelos.config import load_config
from .users import users
from .downloads import downloads
from .groups import groups
from .models import models


@click.group(
    help=""" Comando para realizar consultas SQL y NoSQL relacionadas con estadísticas de uso de BioModelos.""",
    short_help="Consultar estadísticas de uso de BioModelos",
)
@click.pass_context
def stats(ctx):
    if ctx.invoked_subcommand == "models":
        config = load_config()
        if not "MONGODB" in config.sections():
            click.secho(
                "La conexión a la base de datos de MongoDB no ha sido configurada correctamente.",
                fg="red",
                blink=True,
            )
            click.secho(
                "Primero ejecute 'bmdbutils setup mongo'",
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
                mongo_db=config["MONGODB"]["database"],
            )
    if ctx.invoked_subcommand in ["users", "downloads", "groups"]:
        config = load_config()
        if not "POSTGRESDB" in config.sections():
            click.secho(
                "La conexión a la base de datos de Postgres no ha sido configurada correctamente.",
                fg="red",
                blink=True,
            )
            click.secho(
                "Primero ejecute 'bmdbutils setup postgres'",
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
