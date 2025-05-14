"""
$ bmdbutils validate
"""
import click
import pandas as pd


@click.command(
    short_help="Cargar una tabla de modelos, registros o especies a una "
    "colección de mongoDB [WIP]."
)
@click.option(
    "--csv-file",
    prompt="Archivo CSV",
    hide_input=False,
    help="Archivo CSV que contiene los registros de BioModelos",
)
def validate(csv_file):
    try:
        df = pd.read_csv(csv_file)
        if df.empty:
            raise ValueError("El archivo CSV está vacío.")
        if not all(df.columns.isin(["id", "nombre", "apellido", "algo"])):
            raise ValueError(
                "El archivo CSV no contiene las columnas requeridas: id, nombre, apellido, algo."
            )
        else:
            print("El archivo CSV es válido.")
        return True

    except FileNotFoundError:
        print(f"El archivo {csv_file} no se encuentra.")
        return False
    except pd.errors.EmptyDataError:
        print("El archivo CSV está vacío.")
        return False
    except Exception as e:
        print(f"Error al verificar el archivo CSV: {e}")
        return False
