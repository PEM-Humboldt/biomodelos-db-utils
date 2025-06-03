"""
$ bmdbutils mongo upload 
"""
import pandas as pd
import click
import configparser
import os
import appdirs

from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(
    short_help="Cargar documentos en una colección de datos mongoDB de BioModelos."
)
@click.option(
    "--csv-file",
    prompt="Archivo CSV",
    hide_input=False,
    help="Archivo CSV que contiene los registros de BioModelos",
)
@pass_mongo
def upload(mongo, csv_file):
    click.secho(
        "⌛ Validando el archivo CSV...",
        fg="white",
    )
    validation = mongo.validate_csv_data_records(csv_file)
    if type(validation) == bool:
        click.secho(
            "✅ El archivo CSV posee el esquema necesario.",
            fg="green",
            bold=True,
        )
        config_path = os.path.join(
            appdirs.user_config_dir("bmdbutils"), "mongo"
        )
        config = configparser.ConfigParser()
        config.read(config_path)
        click.secho(
            "⌛ Validando registros taxID...",
            fg="yellow",
        )
        tax_id_validation = mongo.validate_tax_ids()
        if tax_id_validation:
            click.secho(
                "⌛ Subiendo documentos a la colección de datos mongoDB...",
                fg="yellow",
            )
            mongo.upload_mongo(csv_file)
        else:
            click.secho(
                "⛔ Falló la validación de taxIDs. Debe crear los taxIDs en la colección 'species' antes de subir los datos.",
                fg="red",
                bold=True,
            )
            return

    elif type(validation) == list:
        click.secho(
            "⛔ El archivo CSV tiene campos u datos no válidos.",
            fg="red",
        )
        click.secho(
            "⚠️  Utilice el comando 'bmdbutils mongo validate' para más detalles.",
            fg="yellow",
            bold=True,
        )

    else:
        click.secho(
            "⛔ Falló la validación del archivo CSV.",
            fg="yellow",
        )
        click.secho(f"{validation}", fg="red")
