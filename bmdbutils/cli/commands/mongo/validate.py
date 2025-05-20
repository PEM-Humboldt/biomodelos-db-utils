"""
$ bmdbutils validate
"""
import click
from bmdbutils.biomodelos.mongo import Mongo


@click.command(
    short_help="Valida un archivo csv de modelos, registros o especies a una colección de mongoDB [WIP]."
)
@click.option(
    "--csv-file",
    prompt="Archivo CSV",
    hide_input=False,
    help="Archivo CSV que contiene los registros de BioModelos",
)
def validate(csv_file):
    validation, result_validate_csv = Mongo.validate_csv_data_records(csv_file)
    if validation:
        click.secho(result_validate_csv,
                    fg="green", bold=True)
    else:
        click.secho("⚠️ Por favor leer atentamente y corregir el archivo CSV.",
                    fg="yellow", bold=True)
        click.secho(result_validate_csv,
                    fg="red", bold=True)
