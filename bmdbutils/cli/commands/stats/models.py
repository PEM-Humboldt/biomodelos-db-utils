"""
$ bmdbutils stats models
"""
import click
import configparser
import os
import appdirs

from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(
    short_help="Obtener estadísticas de los modelos en la plataforma."
)
@pass_mongo
def models(mongo):
    """Obtener las estadisticas de modelos en la plataforma."""
    cnx = mongo.mongo_connection()
    data = mongo.models_stats(cnx)
    for doc in data:
        for key, value in doc.items():
            click.secho(
                f"Se encontraron {value} modelos en {key}.", fg="white"
            )
    cnx.close()
