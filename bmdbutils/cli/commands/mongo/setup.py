"""
$ bmdbutils mongo setup
"""
import configparser
import os

import appdirs
import click


@click.command(short_help="Configura la base de datos Mongo de BioModelos.")
@click.option(
    "--mongo-url",
    type=str,
    default="192.168.11.105:27016",
    show_default=True,
    help="URL de la base de datos Mongo (incluyendo el número del puerto)",
)
@click.option(
    "--mongo-db",
    type=str,
    default="produccion",
    show_default=True,
    help="Base de datos de Mongo",
)
@click.option(
    "--mongo-username",
    type=str,
    default="biomodelos",
    show_default=True,
    help="Usuario para acceder a la base de datos de Mongo",
)
@click.option(
    "--mongo-password",
    type=str,
    prompt="Contraseña para usuario de Mongo",
    hide_input=True,
    help="Contraseña para el usuario para acceder a la base de datos de Mongo",
)
def setup(mongo_url, mongo_username, mongo_password, mongo_db):
    config = configparser.ConfigParser()
    if (
        mongo_url != None
        and mongo_username != None
        and mongo_password != None
        and mongo_db != None
    ):
        config["MONGODB"] = {
            "url": mongo_url,
            "username": mongo_username,
            "password": mongo_password,
            "db": mongo_db,
        }

    target_conf_folder = appdirs.user_config_dir("bmdbutils")
    if not os.path.exists(target_conf_folder):
        os.makedirs(target_conf_folder)

    with open(os.path.join(target_conf_folder, "mongo"), "w") as configfile:
        config.write(configfile)

    click.secho(
        "La configuración de la base de datos MongoDB se ha realizado con éxito.",
        blink=True,
        bold=True,
        fg="green",
    )
