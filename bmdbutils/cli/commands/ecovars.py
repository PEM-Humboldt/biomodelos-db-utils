"""
$ bmdbutils ecovars
"""
from datetime import date
from os import path
from csv import writer

import click

from bmdbutils.biomodelos.biomodelos import Biomodelos
from bmdbutils._helpers import clean_date_range, clean_tax_list

pass_biomodelos = click.make_pass_decorator(Biomodelos)


@click.command(short_help="Obtener la lista de variables ecológicas.")
@click.option(
    "--tax-ids",
    type=str,
    help="lista de ids de especies separados por coma (,) para filtrar las "
    "variables ecológicas",
)
@click.option(
    "--init-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Fecha de inicio para filtrar las variables ecológicas",
)
@click.option(
    "--end-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="Fecha de finalización para filtrar las variables ecológicas",
)
@click.argument("out_folder", type=click.Path(exists=True, file_okay=False))
@pass_biomodelos
def ecovars(biomodelos, tax_ids, init_date, end_date, out_folder):
    """Obtener las variables ecológicas de los modelos correspondientes a las especies indicadas.

    OUT_FOLDER \t Ruta donde se creará el archivo csv con los resultados de la consulta
    """
    [init_date, end_date] = clean_date_range(init_date, end_date)
    tax_ids = clean_tax_list(tax_ids)

    ecovars = biomodelos.query_ecovars(tax_ids, init_date, end_date)
    name = 'ecological_variables_{init_date}_{end_date}{filtered}.csv'.format(
        init_date=init_date, end_date=end_date, filtered='_filtered' if tax_ids else '')
    
    with open(path.join(out_folder, name), 'w') as outfile:
        csv_writer = writer(outfile)
        csv_writer.writerow(ecovars.head())

    with open(path.join(out_folder, name), 'a+') as outfile:
        csv_writer = writer(outfile)
        for index, row in ecovars.iterrows():
            csv_writer.writerow(row)
