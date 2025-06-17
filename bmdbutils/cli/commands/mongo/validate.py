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
    validation = mongo.validate_csv_data_records(csv_file)
    if type(validation) == bool:
        click.secho(
            "✅ El archivo CSV posee el esquema necesario.",
            fg="white",
        )
    elif type(validation) == list:
        click.secho(
            "⚠️  Por favor leer atentamente y corregir el archivo CSV.",
            fg="yellow",
        )
        for err in validation:
            click.secho(
                f"⛔ [Row {err['register']}] Error in '{err['field']}': {err['message']}",
                fg="red",
            )
    else:
        click.secho(f" {validation}", fg="red")
