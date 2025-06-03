import json
import pandas as pd
import sys
from urllib.parse import quote_plus
from json import loads
from jsonschema import Draft7Validator, FormatChecker
from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    OperationFailure,
    ServerSelectionTimeoutError,
)


class Mongo:
    def __init__(
        self,
        mongo_url,
        mongo_user,
        mongo_pass,
        mongo_db="produccion",
        tax_ids=[],
        inserted_list=[],
    ):
        if mongo_url and mongo_user and mongo_pass:
            [self.mongo_addr, self.mongo_port] = mongo_url.rsplit(":", 1)
            if not self.mongo_port:
                self.mongo_port = 27016
            else:
                self.mongo_port = int(self.mongo_port)
        self.mongo_user = mongo_user
        self.mongo_pass = mongo_pass
        self.mongo_db = mongo_db
        self.tax_ids = tax_ids
        self.inserted_list = inserted_list
        self.mongo_str_connection = f"mongodb://{quote_plus(self.mongo_user)}:{quote_plus(self.mongo_pass)}@{self.mongo_addr}:{self.mongo_port}/?authMechanism=SCRAM-SHA-1&authSource={self.mongo_db}"

    def validate_csv_data_records(self, csv_file):
        all_errors = []

        try:
            df_file = pd.read_csv(csv_file)
            df_file.to_json("tmp/output.json", orient="records", lines=True)

            with open("bmdbutils/biomodelos/schemas/records.json", "r") as f:
                schema = json.load(f)
                validator = Draft7Validator(
                    schema, format_checker=FormatChecker()
                )

            with open("tmp/output.json", "r") as f:
                data = [json.loads(line) for line in f]

                for idx, record in enumerate(data):

                    for key in record.keys():
                        if key == "taxID":
                            self.tax_ids.append(record[key])
                    self.tax_ids = list(set(self.tax_ids))
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

        except pd.errors.EmptyDataError:
            error = f"⛔ El archivo '{csv_file}' está vacío."
            return error

        except FileNotFoundError:
            error = f"⛔ El archivo '{csv_file}' no fue encontrado. Verifica la ruta."
            return error

        except Exception as e:
            error = f"⛔ Error al validar el archivo '{csv_file}': {e}"
            return error

    def mongo_connection(self):
        cnx = MongoClient(
            self.mongo_str_connection, serverSelectionTimeoutMS=5000
        )
        try:
            cnx.admin.command("ping")
            print("✅ Conexión con MongoDB exitosa.")
            return cnx

        except ConnectionFailure as cfe:
            print(f"⛔ Server no disponible: {cfe}")
            sys.exit(1)
        except OperationFailure as opfa:
            print(f"⛔ Error de operación en la base de datos MongoDB: {opfa}")
            sys.exit(1)
        except ServerSelectionTimeoutError as sstoe:
            print(f"⛔ No se pudo conectar al servidor MongoDB: {sstoe}")
            sys.exit(1)

    def validate_tax_ids(self):
        cnx = self.mongo_connection()
        db = cnx[self.mongo_db]
        collection = db["species"]
        tax_id_exists = True

        for tax_id in self.tax_ids:
            prueba = collection.find_one({"taxID": tax_id})

            if prueba != None:
                print(
                    f"✅ El registro taxID: {tax_id} existe en la colección 'species'."
                )

            else:
                tax_id_exists = False
                print(
                    f"⛔ No existe el registro taxID: {tax_id} en la colección 'species'. Debe crearlo antes de subir los datos."
                )
        cnx.close()

        return tax_id_exists

    def upload_mongo(self, df):
        inserted_list = []
        cnx = self.mongo_connection()
        db = cnx[self.mongo_db]
        collection = db["records"]

        with open("tmp/output.json", "r") as f:
            data = [json.loads(line) for line in f]
            try:
                for record in data:
                    inserted_record = collection.insert_one(record)
                    inserted_list.append(inserted_record.inserted_id)
                    print(
                        f"✅ Registro con ID: {inserted_record.inserted_id} cargado correctamente a la colección 'records'."
                    )

            except OperationFailure or ConnectionFailure as err:
                print(
                    "Algo salió mal al subir los registros a la colección 'records'. "
                    "Se eliminarán los registros subidos hasta el momento."
                )
                for id in inserted_list:
                    collection.delete_one({"_id": id})
                    print(
                        f"✅ Registro con ID: {id} eliminado correctamente de la colección 'records'."
                    )
                print(f"⛔ Este fue el error: {err}")
                cnx.close()
                sys.exit(1)
            f.close()
        print(f"✅ Se subieron {len(data)} registros a la colección 'records'.")
        cnx.close()
