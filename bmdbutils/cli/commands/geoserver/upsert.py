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
    short_help="Create or update the model file in Geoserver for an"
    "existing model in BioModelos"
)
@click.argument("models_info", type=click.File())
@click.argument("models_folder", type=click.Path(exists=True, file_okay=False))
@pass_geoserver
@pass_biomodelos
def upsert(biomodelos, geoserver, models_info, models_folder):
    """Create or update the model file in Geoserver for an existing model
    in BioModelos

    MODELS_INFO \t csv file that maps the tax_id, model_id and model_file
    for each model to upload

    MODELS_FOLDER \t Path to folder that contains all the files specified
    in MODEL_INFO
    """
    df = pd.read_csv(models_info)
    for row in df.itertuples():
        click.echo(f"Uploading {row.model_file} to Geoserver")
        ws_name = f"taxid-{row.tax_id:0>5}"
        try:
            geoserver.create_ws(name=ws_name)
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
            print("Error:", e)
            return
