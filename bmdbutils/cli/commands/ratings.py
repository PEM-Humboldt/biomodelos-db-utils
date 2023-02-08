"""
$ bmdbutils ratings
"""
from datetime import date, timedelta
from os import path
from csv import writer

import click

from bmdbutils.biomodelos.biomodelos import Biomodelos

pass_biomodelos = click.make_pass_decorator(Biomodelos)


@click.command(short_help="Obtener las calificaciones otorgadas a modelos.")
@click.option(
    "--tax-ids",
    type=str,
    help="lista de ids de especies separados por coma (,) para filtrar las "
    "calificaciones",
)
@click.option(
    "--init-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Fecha de inicio para filtrar las calificaciones",
)
@click.option(
    "--end-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="Fecha de finalización para filtrar las calificaciones",
)
@click.argument("out_folder", type=click.Path(exists=True, file_okay=False))
@pass_biomodelos
def ratings(biomodelos, tax_ids, init_date, end_date, out_folder):
    """Obtener las calificacioens otorgadas a modelos correspondientes a las
    especies indicadas.

    Por defecto traerá todas las calificaciones asignadas en los últimos 30 días.
    """
    end_date = end_date.date()
    if not init_date:
        init_date = end_date - timedelta(days=30)
    else:
        init_date = init_date.date()

    if not tax_ids:
        tax_ids = list()
    else:
        tax_ids = list(
            map(lambda id: id.strip().replace(' ', ''), tax_ids.split(',')))

    ratings = biomodelos.query_ratings(tax_ids, init_date, end_date)
    name = 'ratings_{init_date}_{end_date}{filtered}.csv'.format(
        init_date=init_date, end_date=end_date, filtered='_filtered' if tax_ids else '')

    with open(path.join(out_folder, name), 'w') as outfile:
        csv_writer = writer(outfile)
        csv_writer.writerow(ratings.head())

    with open(path.join(out_folder, name), 'a+') as outfile:
        csv_writer = writer(outfile)
        for index, row in ratings.iterrows():
            csv_writer.writerow(row)
