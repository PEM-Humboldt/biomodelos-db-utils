"""
$ bmdbutils stats users
"""

import click

from bmdbutils.biomodelos.biomodelos import Biomodelos

pass_biomodelos = click.make_pass_decorator(Biomodelos)


@click.command(
    short_help="Obtener estadísticas de usuarios registrados en BioModelos.",
    help="""Obtener las estadísticas sobre usuarios de la plataforma BioModelos.
    
    Ejemplo de uso:
    $ bmdbutils stats users
    """,
)
@pass_biomodelos
def users(biomodelos):
    total_users, expert_users = biomodelos.query_users()

    click.secho(
        f"Se encontraron {total_users['total_users'].sum()} usuarios registrados.",
        fg="white",
    )
    click.secho(
        f"Se encontraron {expert_users['expert_users'].sum()} usuarios expertos.",
        fg="white",
    )
