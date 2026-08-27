"""
$ bmdbutils setup geoserver
"""

import click

from bmdbutils.biomodelos.config import load_config, save_config


@click.command(
    help="""Comando para configurar GeoServer de BioModelos.
    
    Ejemplo de uso:
    $ bmdbutils setup geoserver --url http://localhost:8080/geoserver --username username
    
    No es necesario agregar el parámetro --password, éste se solicita automáticamente.
    """,
    short_help="Configura el GeoServer de BioModelos",
)
@click.option(
    "--url",
    type=str,
    default="http://localhost:8080/geoserver",
    show_default=True,
    help="URL de GeoServer (incluyendo el protocolo http o https y el número del puerto)",
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
    prompt="Contraseña para el usuario de GeoServer",
    hide_input=True,
    help="Contraseña para el usuario de GeoServer",
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
