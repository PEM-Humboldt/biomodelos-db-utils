"""
$ bmdbutils stats models
"""

import click
import os

from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(
    short_help="Obtener estadísticas sobre modelos en BioModelos.",
    help="""Obtener las estadísticas sobre modelos en la plataforma BioModelos.
    
    Ejemplo de uso:
    $ bmdbutils stats models
    """,
)
@pass_mongo
def models(mongo):
    cnx = mongo.mongo_connection()
    data = mongo.models_stats(cnx)
    for doc in data:
        for key, value in doc.items():
            click.secho(f"Se encontraron {value} modelos {key}.", fg="white")
    cnx.close()
