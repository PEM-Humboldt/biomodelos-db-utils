"""
$ bmdbutils mongo validate
"""
import click
from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(
    short_help="Valida un archivo CSV de registros en la colección records en la base de datos Mongo de BioModelos."
)
@click.option(
    "--csv-file",
    prompt="Ruta del archivo CSV",
    hide_input=False,
    help="Archivo CSV que contiene los registros de BioModelos",
)
@pass_mongo
def validate(mongo, csv_file):
    click.secho(
        "⌛ Validando el archivo CSV...",
        fg="yellow",
        bold=True,
    )
    validation = mongo.validate_csv_data(csv_file, "records")
    if isinstance(validation, bool) and validation is True:
        click.secho(
            "✅ El archivo CSV posee el esquema necesario.",
            fg="white",
        )
    elif isinstance(validation, str):
        click.secho(validation, fg="red")
    else:
        click.secho(
            "⛔ Falló la validación del archivo CSV.",
            fg="red",
        )
        click.secho(
            f"Busque el archivo records_error.txt en la ruta ./tmp/ y lealo atentamente y corrija los errores.",
            fg="red",
        )
