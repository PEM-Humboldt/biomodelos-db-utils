"""
$ bmdbutils records upload
"""

import click

from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(
    short_help="Cargar documentos en la colección records en la base de datos Mongo de BioModelos.",
    help="""Cargar documentos en la colección records de MongoDB. 
    
    Antes de ejecutar este comando, asegúrese de que el archivo CSV haya pasado la validación con el comando 'bmdbutils records validate'.
    
    CSV_FILE: Archivo CSV que contiene los registros de BioModelos.

    OUT_FOLDER: Ruta donde se crearán y guardarán los resultados de la validación.
    
    Ejemplo de uso:
    $ bmdbutils records upload /path/to/records.csv /path/to/output/folder
    """,
)
@click.argument("csv_file", type=click.Path(exists=True))
@click.argument("out_folder", type=click.Path(exists=True, file_okay=False))
@pass_mongo
def upload(mongo, csv_file, out_folder):
    cnx = mongo.mongo_connection()
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
        )
        command = "records"
        validation, outFolder = mongo.validate_csv_data(csv_file, command, out_folder)
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
            if tax_id_validation is True:
                click.secho(
                    "⌛ Cargando documentos a la colección records...",
                    fg="yellow",
                )
                mongo.upload_mongo_records(cnx, command, outFolder)
                cnx.close()
            else:
                click.secho("⛔ Falló la validación de taxIDs.", fg="red")
                click.secho(
                    "⚠️  Debe crear los taxIDs en la colección 'species' antes de subir los documentos a la colección records.",
                    fg="yellow",
                )
        else:
            click.secho(
                "⛔ El archivo CSV tiene campos con datos no válidos.",
                fg="red",
            )
            click.secho(
                f"Busque el archivo {outFolder}/records_error.txt, lealo atentamente y corrija los errores.",
                fg="red",
            )
            click.secho(
                "⚠️  Utilice el comando 'bmdbutils records validate' para más detalles.",
                fg="yellow",
            )
    else:
        click.secho(
            "⛔ Falló la validación del archivo CSV.",
            fg="red",
        )
