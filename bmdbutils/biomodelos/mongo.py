import requests
import json
import pandas as pd
import sys
from urllib.parse import quote_plus
from json import loads
from jsonschema import validate, FormatError
from pymongo import MongoClient


class Mongo:
    def __init__(
        self,
        mongo_url=None,
        mongo_user=None,
        mongo_pass=None,
        mongo_db=None,
        csv_file=None,
    ):
        self.csv_file = csv_file
        if mongo_url and mongo_user and mongo_pass and mongo_db:
            [self.mongo_addr, self.mongo_port] = mongo_url.rsplit(":", 1)
            if not self.mongo_port:
                self.mongo_port = 27016
            else:
                self.mongo_port = int(self.mongo_port)
            self.mongo_user = mongo_user
            self.mongo_pass = mongo_pass
            self.mongo_db = "produccion"
            self.mongo_url = mongo_url

    def query_mongo(self):
        mongo_url = f"mongodb://{quote_plus(self.mongo_user)}:{quote_plus(self.mongo_pass)}@{self.mongo_url}/?authMechanism=SCRAM-SHA-1&authSource={self.mongo_db}"
        cnx = MongoClient(mongo_url)
        db = cnx[self.mongo_db]
        collection = db["records"]

        # Example query to find a specific document
        prueba = collection.find({"species": "Hyospathe wendlandiana"})
        cnx.close()

        return prueba

    def validate_csv_data_records(csv_file):

        try:
            df_file = pd.read_csv(csv_file)
            df_file.to_json("output.json", orient="records", lines=True)
            with open("records_schema.json", "r") as f:
                schema = json.load(f)

            with open("output.json", "r") as f:
                data = [json.loads(line) for line in f]

                for record in data:
                    validate(instance=record, schema=schema)

            # Estoy creando un nuevo archivo json como varios json anidados que depronto
            # van a facilitar la carga a mongo
            with open("output_array.json", "w") as f:
                json.dump(data, f, indent=2)

            return True

        except pd.errors.EmptyDataError:
            print("❌ El archivo CSV está vacío.")
            return False
        except FileNotFoundError:
            print(
                f"❌ El archivo '{csv_file}' no fue encontrado. Verifica la ruta."
            )
            return False
        except FormatError as fe:
            print(
                f"❌ El archivo no cumple con el formato JSON. Detalles: {fe}"
            )
            return False
        except Exception as e:
            print(f"❌ Error al validar el archivo CSV: {e}")
            return False

    def upload_mongo(self, df):
        pass
