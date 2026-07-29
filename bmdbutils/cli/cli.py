"""
bmdbutils CLI entry point.
"""
import os
import click

from bmdbutils.biomodelos.config import load_config
from .commands.setup.setup import setup
from .commands.records.records import records
from .commands.stats.stats import stats
from .commands.models.models import models


@click.group()
@click.pass_context
def main(ctx):
    """BioModelos DB Utils (bmdbutils) es una herramienta de línea de comandos (CLI) que actúa como
    conjunto de utilitarios para la plataforma BioModelos, facilitando tareas de configuración,
    validación, carga y consulta de información.

    Primero ejecute 'bmdbutils setup' para configurar la conexión a las bases de datos, al API y al Geoserver de BioModelos.
    """
    config = load_config()
    if ctx.invoked_subcommand != "setup":
        if not config.sections():
            click.secho(
                "La configuración de bmdbutils no ha sido realizada correctamente.",
                fg="red",
            )
            click.secho(
                "Primero ejecute 'bmdbutils setup' para configurar la conexión a las bases de datos al API y al Geoserver de BioModelos.",
                fg="yellow",
                bold=True,
            )
            ctx.exit(0)

main.add_command(setup)
main.add_command(models)
main.add_command(records)
main.add_command(stats)
