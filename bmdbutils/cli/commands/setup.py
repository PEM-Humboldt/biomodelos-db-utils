"""
$ bmdbutils setup
"""
import configparser
import os

import appdirs
import click


@click.command(short_help="Configura el API de BioModelos y la base de datos.")
@click.option(
    "--url",
    type=str,
    default="http://192.168.11.105:4000",
    show_default=True,
    help="URL del API de BioMobelos (incluyendo el número del puerto)",
)
def setup(url):
    config = configparser.ConfigParser()
    config["API"] = {"url": url}

    target_conf_folder = appdirs.user_config_dir("bmdbutils")
    if not os.path.exists(target_conf_folder):
        os.makedirs(target_conf_folder)

    with open(os.path.join(target_conf_folder, "biomodelos"), "w") as configfile:
        config.write(configfile)
