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
from .commands.ratings import ratings
from .commands.editions import editions


@click.group()
@click.pass_context
def main(ctx):
    config = configparser.ConfigParser()
    config.read(os.path.join(appdirs.user_config_dir("bmdbutils"), "biomodelos"))
    if ctx.invoked_subcommand != "setup":
        if len(config.sections()) <= 0:
            click.echo(
                "BioModelos no ha sido configurado. "
                "Primero ejecute 'bmdbutils setup'"
            )
            ctx.exit(0)
    if ctx.invoked_subcommand == "geoserver":
        if not "API" in config.sections():
            click.echo(
                "La url del API de BioModelos no ha sido configurado correctamente. "
                "Primero ejecute 'bmdbutils setup'"
            )
            ctx.exit(0)
        else:
            ctx.obj = Biomodelos(api_url=config["API"]["url"])
    if ctx.invoked_subcommand == "ratings" or ctx.invoked_subcommand == "editions":
        if not "POSTGRESDB" in config.sections():
            click.echo(
                "La conexión a la base de datos de PostgreSQL no ha sido configurada correctamente. "
                "Primero ejecute 'bmdbutils setup'"
            )
            ctx.exit(0)
        else:
            ctx.obj = Biomodelos(
                pg_url=config["POSTGRESDB"]["url"],
                pg_user=config["POSTGRESDB"]["username"],
                pg_pass=config["POSTGRESDB"]["password"]
            )


main.add_command(setup)
main.add_command(upload)
main.add_command(geoserver)
main.add_command(ratings)
main.add_command(editions)
