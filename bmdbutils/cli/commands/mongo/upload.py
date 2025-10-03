"""
$ bmdbutils mongo upload 
"""
import pandas as pd
import click
import configparser
import os
import appdirs
import sys

from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(
    short_help="Cargar documentos en una colección records en la base de datos Mongo de BioModelos."
)
@click.option(
    "--csv-file",
    prompt="Ruta del archivo CSV",
    hide_input=False,
    help="Archivo CSV que contiene los registros de BioModelos",
)
@pass_mongo
def upload(mongo, csv_file):
    config_path = os.path.join(appdirs.user_config_dir("bmdbutils"), "mongo")
    config = configparser.ConfigParser()
    config.read(config_path)
    cnx = mongo.mongo_connection()
    click.secho(
        "⌛ Validando el archivo CSV...",
        fg="yellow",
    )
    validation = mongo.validate_csv_data(csv_file, "records")
    if isinstance(validation, bool):
        click.secho(
            "✅ El archivo CSV posee el esquema necesario.",
            fg="white",
        )
        click.secho(
            "⌛ Validando taxIDs...",
            fg="yellow",
        )
        tax_ids = mongo.extract_tax_ids(csv_file)
        tax_id_validation = mongo.validate_tax_ids(tax_ids, cnx)
        if tax_id_validation:
            click.secho(
                "⌛ Cargando documentos a la colección records...",
                fg="yellow",
            )
            mongo.upload_mongo(cnx)
            cnx.close()
            sys.exit(0)
        else:
            click.secho("⛔ Falló la validación de taxIDs.", fg="red")
            click.secho(
                "⚠️  Debe crear los taxIDs en la colección 'species' antes de subir los documentos a la colección records.",
                fg="yellow",
            )
            return

    elif isinstance(validation, list):
        click.secho(
            "⛔ El archivo CSV tiene campos con datos no válidos.",
            fg="red",
        )
        click.secho(
            "⚠️  Utilice el comando 'bmdbutils mongo validate' para más detalles.",
            fg="yellow",
        )

    else:
        click.secho(
            "⛔ Falló la validación del archivo CSV.",
            fg="red",
        )
        click.secho(f"{validation}", fg="red")
