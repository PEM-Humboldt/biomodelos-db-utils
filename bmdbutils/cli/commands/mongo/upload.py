"""
Upload utilities
"""
import pandas as pd
import pymongo
import click


@click.command(short_help="Upload datos Mongo de BioModelos.")
@click.option(
    "--csv-file",
    prompt="Archivo CSV",
    hide_input=False,
    help="Archivo CSV que contiene los registros de BioModelos",
)
def upload(csv_file):
    #Primer validar
    #luego conectarse a mongo
    #luego cargar
    pass
    
