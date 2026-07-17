"""
$ bmdbutils setup postgres
"""
import configparser
import os
import appdirs
import click

from bmdbutils.biomodelos.config import load_config, save_config


@click.command(
    help="""Comando para configurar la base de datos de BioModelos.
    No es necesario agregar el parámetros --postgres-password, éste se solicita automáticamente.""",
    short_help="Configura la base de datos Postgres de BioModelos.",
)
@click.option(
    "--url",
    type=str,
    default="192.168.11.106:5430",
    show_default=True,
    help="URL de la base de datos de PostgresSQL (incluyendo el número del puerto)",
)
@click.option(
    "--username",
    type=str,
    default="biomodelos_pro",
    show_default=True,
    help="nombre de usuario para acceder a la base de datos de PostgresSQL",
)
@click.option(
    "--password",
    type=str,
    prompt="Contraseña para usuario de base de datos de PostgresSQL",
    hide_input=True,
    help="Contraseña del usuario para acceder a la base de datos de PostgresSQL",
)
def postgres(url, username, password):
    config = load_config()
    config["POSTGRESDB"] = {
        "url": url,
        "username": username,
        "password": password,
    }
    save_config(config)

    click.secho(
        "La configuración de la base de datos Postgres se ha realizado con éxito.",
        blink=True,
        bold=True,
        fg="green",
    )
