"""
$ bmdbutils models fix-metadata
"""

import click

from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(
    short_help="Corregir metadatos a diferentes modelos en la base de datos Mongo de BioModelos.",
    help="""Modificar metadatos de modelos cargados en la base de datos Mongo de BioModelos.

    CSV_FILE: Archivo CSV que contiene los metadatos a corregir de los modelos de BioModelos.

    OUT_FOLDER: Ruta donde se crearán y guardarán los resultados de la carga.

    Ejemplo de uso:
    $ bmdbutils models fix-metadata /path/to/fix_metadata.csv /path/to/output/folder
    """
)
@click.argument("csv_file", type=click.Path(exists=True))
@click.argument("out_folder", type=click.Path(exists=True, file_okay=False))
@pass_mongo
def fix_metadata(mongo, csv_file, out_folder):
    command = "fix-metadata"
    cnx = mongo.mongo_connection()
    click.secho(
        "⌛ Validando el archivo CSV...",
        fg="yellow",
    )
    validation, outFolder = mongo.validate_csv_data(csv_file, command, out_folder)
    if validation is True:
        click.secho(
            "✅ El archivo CSV posee el esquema necesario.",
            fg="white",
        )
        click.secho(
            "⌛ Validando los taxID en la colección species...",
            fg="yellow",
        )
        tax_id = mongo.extract_tax_ids(csv_file)
        model_tax_ids = mongo.extract_model_tax_ids(csv_file)
        tax_id_validation = mongo.validate_tax_ids(tax_id, cnx)

        if tax_id_validation is True:
            click.secho(
                "⌛ Validando los modelID en la colección models...",
                fg="yellow",
            )
            models_validation, models_docs = mongo.validate_models(
                model_tax_ids, cnx
            )
            if models_validation is True:
                click.secho(
                    "⌛ Modificando metadatos de documentos en la colección models...",
                    fg="yellow",
                )
                mongo.update_models_metadata(
                    models_docs, cnx, command, outFolder
                )
                click.secho(
                    f"⚠️ En el archivo {outFolder}/fix-metadata.json se guardaron los documentos cargados.",
                    fg="yellow",
                )
                cnx.close()
            else:
                click.secho("⛔ Falló la validación de modelIDs.", fg="red")
                click.secho(
                    "⚠️ Deben existir los modelIDs en la colección 'models' antes de modificar los documentos.",
                    fg="yellow",
                )
            cnx.close()
        else:
            click.secho("⛔ Falló la validación de taxIDs.", fg="red")
            click.secho(
                "⚠️  Debe crear los taxIDs en la colección 'species' antes de subir los documentos a la colección records.",
                fg="yellow",
            )
    else:
        click.secho(
            "⛔ Falló la validación del archivo CSV.",
            fg="red",
        )
        click.secho(
            f"⚠️ En el archivo {outFolder}/fix-metadata_error.txt se encuentran los errores.",
            fg="red",
        )
