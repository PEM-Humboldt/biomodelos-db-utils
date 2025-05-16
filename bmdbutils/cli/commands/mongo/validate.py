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
    result_validate_csv = Mongo.validate_csv_data_records(csv_file)
    if result_validate_csv:
        click.echo("✅ El archivo CSV posee el exquema necesario.")
    else:
        click.echo("⚠️ Lee atentamente y corrige el archivo CSV.")
