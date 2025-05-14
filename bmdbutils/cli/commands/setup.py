"""
$ bmdbutils setup
"""
import configparser
import os

import appdirs
import click


@click.command(short_help="Configura el API y la base de datos de BioModelos.")
@click.option(
    "--api-url",
    type=str,
    default="http://192.168.11.105:4000",
    show_default=True,
    help="URL del API de BioModelos (incluyendo el número del puerto)",
)
@click.option(
    "--mongo-url",
    type=str,
    default="192.168.11.105:27016",
    show_default=True,
    help="URL de la base de datos Mongo (incluyendo el número del puerto)",
)
@click.option(
    "--postgres-url",
    type=str,
    default="192.168.11.106:5432",
    show_default=True,
    help="URL de la base de datos de PostgresSQL (incluyendo el número del puerto)",
)
@click.option(
    "--postgres-username",
    type=str,
    help="nombre de usuario para acceder a la base de datos de PostgresSQL",
)
@click.option(
    "--postgres-password",
    type=str,
    prompt="Contraseña para usuario de postgres",
    hide_input=True,
    help="contraseña para el usuario para acceder a la base de datos de PostgresSQL",
)
def setup(
    api_url, mongo_url, postgres_url, postgres_username, postgres_password
):
    config = configparser.ConfigParser()
    config["API"] = {"url": api_url}
    config["MONGODB"] = {"url": mongo_url}
    if (
        postgres_url != None
        and postgres_username != None
        and postgres_password != None
    ):
        config["POSTGRESDB"] = {
            "url": postgres_url,
            "username": postgres_username,
            "password": postgres_password,
        }

    target_conf_folder = appdirs.user_config_dir("bmdbutils")
    if not os.path.exists(target_conf_folder):
        os.makedirs(target_conf_folder)

    with open(
        os.path.join(target_conf_folder, "biomodelos"), "w"
    ) as configfile:
        config.write(configfile)
