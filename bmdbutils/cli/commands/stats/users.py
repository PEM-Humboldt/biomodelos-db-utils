"""
$ bmdbutils stats users
"""
import click

from bmdbutils.biomodelos.biomodelos import Biomodelos

pass_biomodelos = click.make_pass_decorator(Biomodelos)


@click.command(
    short_help="Obtener estadísticas de usuarios registrados en la plataforma."
)
@pass_biomodelos
def users(biomodelos):
    """Obtener las estadisticas de usuarios registrados."""
    total_users, expert_users = biomodelos.query_users()

    click.secho(
        f"Se encontraron {total_users['total_users'].sum()} usuarios registrados",
        fg="white",
    )
    click.secho(
        f"Se encontraron {expert_users['total_expertise'].sum()} usuarios expertos.",
        fg="white",
    )
    click.secho(
        f"Se encontraron {total_users['total_users'].sum() - expert_users['total_expertise'].sum()} usuarios sin experticia",
        fg="white",
    )
