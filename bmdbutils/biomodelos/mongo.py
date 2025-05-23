import requests
import json
import pandas as pd
import sys
from urllib.parse import quote_plus
from json import loads
from jsonschema import Draft7Validator, FormatChecker
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

    def validate_csv_data_records(self, csv_file):
        all_errors = []
        try:
            df_file = pd.read_csv(csv_file)
            df_file.to_json("bmdbutils/biomodelos/schemas/output.json", orient="records", lines=True)

            with open("bmdbutils/biomodelos/schemas/records.json", "r") as f:
                schema = json.load(f)
                validator = Draft7Validator(schema, format_checker = FormatChecker())

            with open("bmdbutils/biomodelos/schemas/output.json", "r") as f:
                data = [json.loads(line) for line in f]

                for idx, record in enumerate(data):
                    errors = list(validator.iter_errors(record))
                    for error in errors:
                        all_errors.append(
                            {
                                "registro": idx,
                                "campo": "/".join(map(str, error.path)),
                                "mensaje": error.message,
                            }
                        )

                if len(all_errors) > 0:
                    return all_errors

                else:
                    return True

            with open("bmdbutils/biomodelos/schemas/output_array.json", "w") as f:
                json.dump(data, f, indent=2)

        except pd.errors.EmptyDataError:

            error = f"❌ El archivo '{csv_file}' está vacío."
            return error

        except FileNotFoundError:
            error = f"❌ El archivo '{csv_file}' no fue encontrado. Verifica la ruta."
            return error

        except Exception as e:
            error = f"❌ Error al validar el archivo '{csv_file}': {e}"
            return error

    def upload_mongo(self, df):
        pass
