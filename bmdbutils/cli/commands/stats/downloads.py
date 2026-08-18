"""
$ bmdbutils stats downloads
"""

import click

from bmdbutils.biomodelos.biomodelos import Biomodelos

pass_biomodelos = click.make_pass_decorator(Biomodelos)


@click.command(
    short_help="Obtener estadísticas sobre descargas de modelos de BioModelos.",
    help="""Obtener las estadísticas sobre descargas de modelos en la plataforma BioModelos.
    
    Ejemplo de uso:
    $ bmdbutils stats downloads
    """,
)
@pass_biomodelos
def downloads(biomodelos):
    downloads = biomodelos.query_downloads()

    click.secho(
        f"Se han descargado un total de {downloads['total_downloads'].sum()} modelos para los siguientes usos:",
        fg="white",
    )
    for row in downloads.itertuples(index=False):
        click.secho(f"{row[1]} se descargaron {row[0]} modelos.", fg="white")
