"""
$ bmdbutils setup api
"""

import click

from bmdbutils.biomodelos.config import load_config, save_config


@click.command(
    help="""Comando para configurar el API de BioModelos.
    
    Ejemplo de uso:
    $ bmdbutils setup api --url http://localhost:3333  
    """,
    short_help="Configura la API de BioModelos.",
)
@click.option(
    "--url",
    type=str,
    default="http://192.168.11.105:4000",
    show_default=True,
    help="URL del API de BioModelos (incluyendo el protocolo http o https y el número del puerto)",
)
def api(url):
    config = load_config()
    config["API"] = {"url": url}
    save_config(config)
    click.secho(
        "La configuración del API se ha realizado con éxito.",
        bold=True,
        fg="green",
    )
