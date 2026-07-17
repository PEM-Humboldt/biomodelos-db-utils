"""
$ bmdbutils setup
"""
import configparser
import os
import appdirs
import click

from .setup_geoserver import geoserver
from .setup_mongo import mongo
from .setup_postgres import postgres
from .setup_api import api


@click.group(
    help=""" Comando para configurar las conexiones de BioModelos.""",
    short_help="Configuración de conexiones de BioModelos.",
    invoke_without_command=True,
)
@click.pass_context
def setup(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


setup.add_command(mongo)
setup.add_command(geoserver)
setup.add_command(postgres)
setup.add_command(api)
