"""
$ bmbdutils geoserver upsert
"""
import os

import click
import pandas as pd

from bmdbutils.biomodelos.biomodelos import Biomodelos
from bmdbutils.biomodelos.geoserver import Geoserver

pass_biomodelos = click.make_pass_decorator(Biomodelos)
pass_geoserver = click.make_pass_decorator(Geoserver)


@click.command(
    short_help="Crear o actualizar los archivos de modelos en el GeoServer para "
    "modelos existentes en BioModelos"
)
@click.argument("models_info", type=click.File())
@click.argument("models_folder", type=click.Path(exists=True, file_okay=False))
@pass_geoserver
@pass_biomodelos
def upsert(biomodelos, geoserver, models_info, models_folder):
    """Crear o actualizar los archivos de modelos en el GeoServer para modelos
    existentes en BioModelos

    MODELS_INFO \t archivo csv que mapea los campos tax_id, model_id y
    model_file para cada modelo a cargar

    MODELS_FOLDER \t Ruta a la carpeta que contiene los archivos especificados
    en el campo model_file del archivo MODEL_INFO
    """
    df = pd.read_csv(models_info)
    for row in df.itertuples():
        click.echo(f"Uploading {row.model_file} to Geoserver")
        ws_name = f"taxid-{row.tax_id:0>5}"
        try:
            geoserver.create_ws(name=ws_name)
            geoserver.upsert_workspaces_rules(
                workspace=ws_name,
                permission="r",
                role_name="READ_TAXID",
                mode="R",
            )
            geoserver.load_layer(
                file_path=os.path.join(models_folder, row.model_file),
                workspace_name=ws_name,
                layer_name=row.model_id,
            )

            click.echo(f"Updating {row.model_id} layer name")
            biomodelos.update_model_layer(
                model_id=row.model_id, layer=f"{ws_name}:{row.model_id}"
            )
        except Exception as e:
            click.secho(str(e), fg="red")
            return
