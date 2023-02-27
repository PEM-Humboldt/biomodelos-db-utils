"""
$ bmdbutils editions
"""
from datetime import date, timedelta
from os import path, makedirs
import json

import click

from bmdbutils.biomodelos.biomodelos import Biomodelos
from bmdbutils._helpers import clean_date_range, clean_tax_list, clean_str

pass_biomodelos = click.make_pass_decorator(Biomodelos)


@click.command(short_help="Obtener las ediciones hechas a modelos.")
@click.option(
    "--tax-ids",
    type=str,
    help="lista de ids de especies separados por coma (,) para filtrar las "
    "ediciones",
)
@click.option(
    "--init-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Fecha de inicio para filtrar las ediciones",
)
@click.option(
    "--end-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="Fecha de finalización para filtrar las ediciones",
)
@click.argument("out_folder", type=click.Path(exists=True, file_okay=False))
@pass_biomodelos
def editions(biomodelos, tax_ids, init_date, end_date, out_folder):
    """Obtener las ediciones hechas a modelos correspondientes a las especies indicadas.

    Por defecto traerá todas las ediciones hechas en los últimos 30 días.

    OUT_FOLDER \t Ruta donde se crearán guardarán los resultados de la consulta (un archivo
    geojson por edición)
    """
    [init_date, end_date] = clean_date_range(init_date, end_date)
    tax_ids = clean_tax_list(tax_ids)

    editions = biomodelos.query_editions(tax_ids, init_date, end_date)
    folder = 'editions_{init_date}_{end_date}{filtered}'.format(
        init_date=init_date, end_date=end_date, filtered='_filtered' if tax_ids else '')
    if not path.exists(path.join(out_folder, folder)):
        makedirs(path.join(out_folder, folder))

    for index, row in editions.iterrows():
        geojson = row['geoJSON']
        geojson = json.loads(geojson)
        filename = 'sp-{species_id}_usr-{user_id}_thr-{threshold}.geojson'.format(
            species_id=str(row['species_id']), user_id=str(row['user_id']), threshold=clean_str(row['threshold']))
        if len(geojson['features']) < 1:
            print("has no features")
            geojson['features']
            feat = {}
            feat['properties'] = {
                'UserID': row['user_id'],
                'userName': row['name'],
                'taxID': row['species_id'],
                'threshold': row['threshold']
            }
            feat['type'] = 'Feature'
            feat['geometry'] = {}
            geojson['features'].append(feat)
            with open(path.join(out_folder, folder, filename), 'w') as outfile:
                json.dump(geojson, outfile, ensure_ascii=False)

        else:
            for idx, feat in enumerate(geojson['features']):
                print("has features")
                feat['properties']['userID'] = row['user_id']
                feat['properties']['userName'] = row['name']
                feat['properties']['taxID'] = row['species_id']
                feat['properties']['threshold'] = row['threshold']
                with open(path.join(out_folder, folder, filename), 'w') as outfile:
                    json.dump(geojson, outfile, ensure_ascii=False)
