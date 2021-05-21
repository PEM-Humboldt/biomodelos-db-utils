"""
$ bmdbutils geoserver setup
"""
import configparser
import os

import appdirs
import click


@click.command(short_help="Setup Geoserver config values")
@click.option(
    "--url",
    type=str,
    default="http://192.168.11.58:8181/geoserver",
    show_default=True,
    help="Geoserver url",
)
@click.option(
    "--username",
    type=str,
    default="admin",
    show_default=True,
    help="username to access Geoserver",
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    help="password for username",
)
def setup(url, username, password):
    config = configparser.ConfigParser()
    config["LOCATION"] = {"url": url}
    config["CREDENTIALS"] = {"username": username, "password": password}

    target_conf_folder = appdirs.user_config_dir("bmdbutils")
    if not os.path.exists(target_conf_folder):
        os.makedirs(target_conf_folder)

    with open(os.path.join(target_conf_folder, "geoserver"), "w") as configfile:
        config.write(configfile)
