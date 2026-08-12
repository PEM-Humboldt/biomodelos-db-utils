"""
$ bmdbutils records validate
"""

import click
from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(
    short_help="Validar un archivo CSV de registros en la colección records en la base de datos Mongo de BioModelos.",
    help="""Validar un archivo CSV de registros en la colección records en la base de datos Mongo de BioModelos.
    
    CSV_FILE: Archivo CSV que contiene los registros de BioModelos.
    
    OUT_FOLDER: Ruta donde se crearán y guardarán los resultados de la validación.
    
    Ejemplo de uso:
    $ bmdbutils records validate /path/to/records.csv /path/to/output/folder 
    """,
)
@click.argument("csv_file", type=click.Path(exists=True))
@click.argument("out_folder", type=click.Path(exists=True, file_okay=False))
@pass_mongo
def validate(mongo, csv_file, out_folder):
    click.secho(
        "⌛ Validando columnas year, month y day del archivo CSV...",
        fg="yellow",
        bold=True,
    )
    validateDate = mongo.validate_date_fields(csv_file)
    if validateDate is True:
        click.secho(
            "⌛ Validando el archivo CSV...",
            fg="yellow",
            bold=True,
        )
        command = "records"
        validation, folder = mongo.validate_csv_data(csv_file, command, out_folder)
        if validation is True:
            click.secho(
                "✅ El archivo CSV posee el esquema necesario.",
                fg="white",
            )
        else:
            click.secho(
                "⛔ Falló la validación del archivo CSV.",
                fg="red",
            )
            click.secho(
                f"Busque el archivo ./{folder}/records_error.txt, lealo atentamente y corrija los errores.",
                fg="red",
            )
    else:
        click.secho(
            "⛔ Falló la validación del archivo CSV.",
            fg="red",
        )
