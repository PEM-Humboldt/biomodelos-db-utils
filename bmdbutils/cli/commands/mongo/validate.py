"""
$ bmdbutils mongo validate
"""
import click
from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)

@click.command(
    short_help="Valida un archivo csv de modelos, registros o especies a una colección de mongoDB [WIP]."
)
@click.option(
    "--csv-file",
    prompt="Archivo CSV",
    hide_input=False,
    help="Archivo CSV que contiene los registros de BioModelos",
)
@pass_mongo
def validate(mongo, csv_file):
    validation = mongo.validate_csv_data_records(csv_file)
    if type(validation) == bool:
        click.secho(
            "✅ El archivo CSV posee el esquema necesario.",
            fg="green",
            bold=True,
        )
    elif type(validation) == list:
        click.secho(
            "⚠️  Por favor leer atentamente y corregir el archivo CSV.",
            fg="yellow",
            bold=True,
        )
        for err in validation:
            click.secho(
                f"[Registro {err['registro']}] Error en '{err['campo']}': {err['mensaje']}",
                fg="red",
                bold=False,
            )
    else:
        click.secho(validation, fg="red", bold=True)
