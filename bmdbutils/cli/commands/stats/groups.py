"""
$ bmdbutils stats groups
"""

import click

from bmdbutils.biomodelos.biomodelos import Biomodelos

pass_biomodelos = click.make_pass_decorator(Biomodelos)


@click.command(
    short_help="Obtener estadísticas sobre los grupos de usuarios en BioModelos.",
    help="""Obtener las estadísticas sobre los grupos de usuarios en la plataforma BioModelos.
    
    Ejemplo de uso:
    $ bmdbutils stats groups
    """,
)
@pass_biomodelos
def groups(biomodelos):
    total_groups, active_groups = biomodelos.query_groups()
    click.secho(
        f"Se encontraron {total_groups['total_groups'].sum()} grupos registrados.",
        fg="white",
    )
    click.secho(
        f"Se encontraron {active_groups['active_groups'].sum()} grupos activos.",
        fg="white",
    )
