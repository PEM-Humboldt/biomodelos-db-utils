"""
$ bmdbutils mongo metadatos 
"""
import click
import configparser
import os
import appdirs
import sys

from bmdbutils.biomodelos.mongo import Mongo

pass_mongo = click.make_pass_decorator(Mongo)


@click.command(
    short_help="Corregir metadatos a diferentes modelos en la base de datos Mongo de BioModelos."
)
@click.option(
    "--csv-file",
    prompt="Ruta del archivo CSV",
    hide_input=False,
    help="Archivo CSV que contiene los registros de BioModelos",
)
@pass_mongo
def metadatos(mongo, csv_file):
    config_path = os.path.join(
            appdirs.user_config_dir("bmdbutils"), "mongo"
        )
    config = configparser.ConfigParser()
    config.read(config_path)
    cnx = mongo.mongo_connection()
    click.secho(
        "⌛ Validando el archivo CSV...",
        fg="yellow",
    )
    validation = mongo.validate_metadatos_models(csv_file)
    if validation is True:
        click.secho(
            "✅ El archivo CSV posee el esquema necesario.",
            fg="white",
        )
        click.secho(
            "⌛ Validando taxIDs...",
            fg="yellow",
        )
        tax_id = mongo.extract_tax_ids(csv_file)
        model_tax_ids = mongo.extract_model_tax_ids(csv_file)
        tax_id_validation = mongo.validate_tax_ids(tax_id, cnx)
        
        if tax_id_validation:
            click.secho(
                "⌛ Validando modelIDs...",
                fg="yellow",
            )
            models_validation, models_docs = mongo.validate_models(model_tax_ids, cnx)
            if models_validation:
                click.secho(
                    "⌛ Modificando metadatos de documentos en la colección models...",
                    fg="yellow",
                )
                mongo.update_metadata_models(models_docs, cnx)
                click.secho(
                    "⚠️ En el archivo ~/biomodelos-db-utils/tmp/output.json se guardaron los documentos cargados.",
                    fg="yellow",
                )
                cnx.close()
                sys.exit(0)
            else:
                click.secho(
                    "⛔ Falló la validación de modelIDs.",
                    fg="red"
                )
                click.secho(
                    "⚠️  Deben existir los modelIDs en la colección 'models' antes de modificar los documentos.",
                    fg="yellow"
                )
            cnx.close()
            sys.exit(0)                
        else:
            click.secho(
                "⛔ Falló la validación de taxIDs.",
                fg="red"
            )
            click.secho(
                "⚠️  Debe crear los taxIDs en la colección 'species' antes de subir los documentos a la colección records.",
                fg="yellow"
            )
    
    elif isinstance(validation, str):
        click.secho(validation, fg="red")
    else:    
        click.secho(
            "⛔ Falló la validación del archivo CSV.",
            fg="red",
        )
        click.secho(f"busque el archivo ~/biomodelos-db-utils/tmp/metadata_error.txt y lealo atentamente", fg="red")
