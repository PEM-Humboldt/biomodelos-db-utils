"""
$ bmdbutils setup
"""

import click

from .setup_geoserver import geoserver
from .setup_mongo import mongo
from .setup_postgres import postgres
from .setup_api import api


@click.group(
    help="""Comando para configurar las conexiones a las bases de datos Postgres y Mongo, al API y al Geoserver de BioModelos.""",
    short_help="Configuración de conexiones de BioModelos.",
)
@click.pass_context
def setup(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


setup.add_command(mongo)
setup.add_command(geoserver)
setup.add_command(postgres)
setup.add_command(api)
