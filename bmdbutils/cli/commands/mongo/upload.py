"""
Upload utilities
"""
import pandas as pd
import pymongo
import click
import configparser
import os
import appdirs

from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(short_help="Upload datos Mongo de BioModelos.")
@click.option(
    "--csv-file",
    prompt="Archivo CSV",
    hide_input=False,
    help="Archivo CSV que contiene los registros de BioModelos",
)
@pass_mongo
def upload(mongo, csv_file):
    config_path = os.path.join(appdirs.user_config_dir("bmdbutils"), "mongo")
    config = configparser.ConfigParser()
    config.read(config_path)
    # mongo_user = config['MONGODB']['username']
    # df = pd.read_csv(read_csv)
    prueba = mongo.query_mongo()
    for i in prueba:
        click.echo(i)
    # Primer validar
    # luego conectarse a mongo
    # luego cargar
