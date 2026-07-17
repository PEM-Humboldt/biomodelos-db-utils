"""
$ bmdbutils models 
"""
import configparser
import os

import appdirs
import click

from bmdbutils.biomodelos.geoserver import Geoserver
from bmdbutils.biomodelos.biomodelos import Biomodelos
from bmdbutils.biomodelos.mongo import Mongo
from bmdbutils.biomodelos.config import load_config
from .ecovars import ecovars
from .editions import editions
from .ratings import ratings
from .geoserver_upsert import geoserver_upsert
from .fix_metadata import models_metadata



@click.group(
    short_help="Operaciones relacionadas con modelos de BioModelos",
)
@click.pass_context
def models(ctx):
    config = load_config()
    if ctx.invoked_subcommand in ["ratings", "editions", "ecovars"]:
        if not "POSTGRESDB" in config.sections():
            click.secho(
                "La conexión a la base de datos de PostgreSQL no ha sido configurada correctamente. "
                "Primero ejecute 'bmdbutils setup'",
                fg="red",
                bold=False,
            )
            ctx.exit(0)
        else:
            ctx.obj = Biomodelos(
                pg_url=config["POSTGRESDB"]["url"],
                pg_user=config["POSTGRESDB"]["username"],
                pg_pass=config["POSTGRESDB"]["password"],
            )
    if ctx.invoked_subcommand == "geoserver-upsert":
        if (not "GEOSERVER" in config.sections()):
            click.secho(
                "Geoserver no ha sido configurado o la configuración es errónea. "
                "Primero ejecute 'bmdbutils geoserver setup'",
                fg="red",
                bold=False,
            )
            ctx.exit(0)
        elif not "API" in config.sections():
            click.secho(
                "La url del API de BioModelos no ha sido configurado correctamente. "
                "Primero ejecute 'bmdbutils setup api'",
                fg="red",
                bold=False,
            )
            ctx.exit(0)
        else:
            ctx.ensure_object(dict)
            ctx.obj["biomodelos"] = Biomodelos(
                api_url=config["API"]["url"]
            )
            ctx.obj["geoserver"] = Geoserver(
                config["GEOSERVER"]["url"],
                config["GEOSERVER"]["username"],
                config["GEOSERVER"]["password"],
            )
    
    if ctx.invoked_subcommand == "fix-metadata":
        if not "MONGODB" in config.sections():
            click.secho(
                "La conexión a la base de datos de MongoDB no ha sido configurada correctamente. "
                "Primero ejecute 'bmdbutils setup mongo'",
                fg="red",
                bold=False,
            )
            ctx.exit(0)
        else:
            ctx.obj = Mongo(
                mongo_url=config["MONGODB"]["url"],
                mongo_user=config["MONGODB"]["username"],
                mongo_pass=config["MONGODB"]["password"],
                mongo_db=config["MONGODB"]["database"],
            )

models.add_command(ratings)
models.add_command(editions)
models.add_command(ecovars)
models.add_command(geoserver_upsert, name="geoserver-upsert")
models.add_command(models_metadata, name="fix-metadata")
