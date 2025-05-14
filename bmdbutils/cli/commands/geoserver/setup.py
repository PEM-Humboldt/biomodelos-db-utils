"""
$ bmdbutils geoserver setup
"""
import configparser
import os

import appdirs
import click


@click.command(short_help="Configurar GeoServer")
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
    help="nombre de usuario para acceder a GeoServer",
)
@click.option(
    "--password",
    prompt="Contraseña para el ususario de GeoServer",
    hide_input=True,
    help="contraseña para el ususario",
)
def setup(url, username, password):
    config = configparser.ConfigParser()
    config["LOCATION"] = {"url": url}
    config["CREDENTIALS"] = {"username": username, "password": password}

    target_conf_folder = appdirs.user_config_dir("bmdbutils")
    if not os.path.exists(target_conf_folder):
        os.makedirs(target_conf_folder)

    with open(
        os.path.join(target_conf_folder, "geoserver"), "w"
    ) as configfile:
        config.write(configfile)
