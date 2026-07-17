"""
$ bmdbutils setup mongo
"""
import configparser
import os
import appdirs
import click

from bmdbutils.biomodelos.config import load_config, save_config


@click.command(
    help="""Comando para configurar la base de datos MongoDB de BioModelos. 
        No es necesario ejecutar este comando si ya se ha configurado la base de datos MongoDB. 
        No es necesario agregar el parámetro --mongo-password, éste se solicita automáticamente""",
    short_help="Configura la base de datos Mongo de BioModelos.",
)
@click.option(
    "--url",
    type=str,
    default="192.168.11.105:27016",
    show_default=True,
    help="URL de la base de datos Mongo (incluyendo el número del puerto)",
)
@click.option(
    "--database",
    type=str,
    default="produccion",
    show_default=True,
    help="Base de datos de Mongo",
)
@click.option(
    "--username",
    type=str,
    default="biomodelos",
    show_default=True,
    help="Usuario para acceder a la base de datos de Mongo",
)
@click.option(
    "--password",
    type=str,
    prompt="Contraseña para usuario de Mongo",
    hide_input=True,
    help="""Contraseña para el usuario para acceder a la base de datos de Mongo,
    se solicita automaticamente.""",
)
def mongo(url, username, password, database):
    config = load_config()
    config["MONGODB"] = {
        "url": url,
        "username": username,
        "password": password,
        "database": database,
    }
    save_config(config)

    click.secho(
        "La configuración de la base de datos MongoDB se ha realizado con éxito.",
        blink=True,
        bold=True,
        fg="green",
    )
