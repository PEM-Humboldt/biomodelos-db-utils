"""
$ bmdbutils records upload
"""

import pandas as pd
import click
import os
import sys

from bmdbutils.biomodelos.mongo import Mongo
from bmdbutils.biomodelos.config import load_config

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(
    short_help="Cargar documentos en una colección records en la base de datos Mongo de BioModelos."
)
@click.option(
    "--csv-file",
    type=str,
    help="Archivo CSV que contiene los registros de BioModelos",
)
@click.argument("out_folder", type=click.Path(exists=True, file_okay=False))
@pass_mongo
def upload(mongo, csv_file, out_folder):
    config = load_config()
    cnx = mongo.mongo_connection()
    click.secho(
        "⌛ Validando columnas year, month y day del archivo CSV...",
        fg="yellow",
        bold=True,
    )
    validateDate = mongo.validate_date_fields(csv_file)
    if isinstance(validateDate, bool) and validateDate is True:
        click.secho(
            "⌛ Validando el archivo CSV...",
            fg="yellow",
        )
        command = "records"
        validation = mongo.validate_csv_data(csv_file, command, out_folder)
        if validation is True:
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
                mongo.upload_mongo_records(cnx, command, out_folder)
                cnx.close()
                sys.exit(0)
            else:
                click.secho("⛔ Falló la validación de taxIDs.", fg="red")
                click.secho(
                    "⚠️  Debe crear los taxIDs en la colección 'species' antes de subir los documentos a la colección records.",
                    fg="yellow",
                )
                sys.exit(1)
        else:
            click.secho(
                "⛔ El archivo CSV tiene campos con datos no válidos.",
                fg="red",
            )
            click.secho(
                "⚠️  Utilice el comando 'bmdbutils records validate' para más detalles.",
                fg="yellow",
            )
            sys.exit(1)
    else:
        click.secho(
            "⛔ Falló la validación del archivo CSV.",
            fg="red",
        )
        sys.exit(1)
