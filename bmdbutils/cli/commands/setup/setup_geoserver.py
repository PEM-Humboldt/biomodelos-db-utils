"""
$ bmdbutils setup geoserver
"""

import os
import click

from bmdbutils.biomodelos.config import load_config, save_config


@click.command(
    help=""" Comando para configurar GeoServer de BioModelos.
        No es necesario ejecutar este comando si ya se ha configurado el GeoServer.
        No es necesario agregar el parámetro --password, éste se solicita automáticamente""",
    short_help="Configura el GeoServer de BioModelos",
)
@click.option(
    "--url",
    type=str,
    default="http://192.168.11.58:8181/geoserver",
    show_default=True,
    help="URL de GeoServer",
)
@click.option(
    "--username",
    type=str,
    default="admin",
    show_default=True,
    help="Nombre de usuario para acceder a GeoServer",
)
@click.option(
    "--password",
    prompt="Contraseña para el ususario de GeoServer",
    hide_input=True,
    help="Contraseña para el ususario",
)
def geoserver(url, username, password):
    config = load_config()
    config["GEOSERVER"] = {
        "url": url,
        "username": username,
        "password": password,
    }
    save_config(config)

    click.secho(
        "La configuración de GeoServer se ha realizado con éxito.",
        bold=True,
        fg="green",
    )
