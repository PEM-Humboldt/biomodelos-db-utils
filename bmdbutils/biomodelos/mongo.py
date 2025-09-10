import json
import pandas as pd
import sys
from urllib.parse import quote_plus
from jsonschema import Draft7Validator, FormatChecker
from pymongo import MongoClient, UpdateOne
from pymongo.errors import (
    PyMongoError,
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
        self.mongo_str_connection = f"mongodb://{quote_plus(self.mongo_user)}:{quote_plus(self.mongo_pass)}@{self.mongo_addr}:{self.mongo_port}/?authMechanism=SCRAM-SHA-1&authSource={self.mongo_db}"

    def mongo_connection(self):
        cnx = MongoClient(
            self.mongo_str_connection, serverSelectionTimeoutMS=5000
        )
        try:
            cnx.admin.command("ping")
            print("✅ Conexión con MongoDB exitosa.")
            return cnx

        except ConnectionFailure as cfe:
            print(f"⛔ Servidor no disponible: {cfe}")
            sys.exit(1)
        except ServerSelectionTimeoutError as e:
            print("No se pudo conectar al servidor MongoDB:", e)
            sys.exit(1)

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
                f.close()
            with open("tmp/output.json", "r") as f:
                data = [json.loads(line) for line in f]

                for idx, record in enumerate(data):
                    errors = list(validator.iter_errors(record))
                    for error in errors:
                        all_errors.append(
                            {
                                "record": idx,
                                "field": "/".join(map(str, error.path)),
                                "message": error.message,
                            }
                        )
                f.close()
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

    def extract_tax_ids(self, csv_file):
        df_file = pd.read_csv(csv_file)
        if "taxID" in df_file.columns:
            tax_ids = df_file["taxID"].unique().tolist()
            return tax_ids
        else:
            print("⛔ No se encontró la columna 'taxID' en el archivo CSV.")
            sys.exit(1)

    def extract_model_tax_ids(self, csv_file):
        df_file = pd.read_csv(csv_file)
        docs = df_file[["modelID", "taxID"]].to_dict(orient="records")
        return docs

    def validate_tax_ids(self, tax_ids, cnx):
        tax_id_exists = True
        try:
            db = cnx[self.mongo_db]
            collection = db["species"]
            existing_docs = collection.find({"taxID": {"$in": tax_ids}})
            tax_id_found = [doc["taxID"] for doc in existing_docs]
            tax_id_not_found = set(tax_ids) - set(tax_id_found)

            if len(tax_id_not_found) > 0:
                print(
                    f"⛔ En la colección 'species' no existen los siguientes taxID: {', '.join(map(str, tax_id_not_found))}. "
                )
                cnx.close()
                tax_id_exists = False
            else:
                print(
                    f"✅ Los taxID: {', '.join(map(str, tax_id_found))} existen en la colección 'species'."
                )
                return tax_id_exists

        except OperationFailure as opfa:
            print(f"⛔ Error de operación en la base de datos MongoDB: {opfa}")
            sys.exit(1)

    def upload_mongo(self, cnx):
        inserted_list = []
        db = cnx[self.mongo_db]
        collection = db["records"]

        with open("tmp/output.json", "r") as f:
            data = [json.loads(line) for line in f]
            try:
                for record in data:
                    record["createdDate"] = pd.Timestamp.now().isoformat()
                    inserted_record = collection.insert_one(record)
                    inserted_list.append(inserted_record.inserted_id)
                    print(
                        f"✅ Documento con _id: {inserted_record.inserted_id} cargado correctamente a la colección 'records'."
                    )

            except PyMongoError as err:
                print(
                    "Algo salió mal al subir los documentos a la colección 'records'."
                    "Se eliminarán los documentos subidos hasta el momento."
                )
                for id in inserted_list:
                    collection.delete_one({"_id": id})
                    print(
                        f"✅ Documento con _id: {id} eliminado correctamente de la colección 'records'."
                    )
                print(f"⛔ Este fue el error: {err}")
                cnx.close()
                sys.exit(1)
            f.close()
        print(
            f"✅ Se subieron {len(data)} documentos a la colección 'records'."
        )
        cnx.close()

    def validate_metadatos_models(self, csv_file):
        try:
            df_file = pd.read_csv(csv_file)
            df_file.to_json("tmp/output.json", orient="records", lines=True)

            with open(
                "bmdbutils/biomodelos/schemas/metadatos_models.json", "r"
            ) as f:
                schema = json.load(f)
                validator = Draft7Validator(
                    schema, format_checker=FormatChecker()
                )
                f.close()
            with open("tmp/output.json", "r") as f:
                data = [json.loads(line) for line in f]
                f.close()
            with open("tmp/metadata_error.txt", "w") as f:
                for idx, record in enumerate(data):
                    errors = list(validator.iter_errors(record))
                    for error in errors:
                        f.write(
                            f"record: {idx}, field: {'/'.join(map(str, error.path))}, message: {error.message}\n"
                        )
                f.close()

            if len(errors) == 0:
                return True
            else:
                return False

        except pd.errors.EmptyDataError:
            error = f"⛔ El archivo '{csv_file}' está vacío."
            return error

        except FileNotFoundError:
            error = f"⛔ El archivo '{csv_file}' no fue encontrado. Verifica la ruta."
            return error

        except Exception as e:
            error = f"⛔ Error al validar el archivo '{csv_file}': {e}"
            return error

    def validate_models(self, docs, cnx):
        models_validation = True
        try:
            db = cnx[self.mongo_db]
            collection = db["models"]
            existing_docs = collection.find({"$or": docs})

            for doc in existing_docs:
                print(
                    f"✅ En la colección models existe un documento con modelID: {doc['modelID']} y taxID: {doc['taxID']}."
                )
            models_docs = list(existing_docs)
            return models_validation, models_docs
        except OperationFailure as opfa:
            print(f"⛔ Error de operación en la base de datos MongoDB: {opfa}")
            sys.exit(1)

    def update_metadata_models(self, models_docs, cnx):
        db = cnx[self.mongo_db]
        collection = db["models"]
        operations = []
        rollback = []
        with open("tmp/output.json", "r") as f:
            for record in f:
                doc = json.loads(record)
                filter = {"modelID": doc["modelID"], "taxID": doc["taxID"]}
                changes = {
                    key: value
                    for key, value in doc.items()
                    if key not in filter
                }
                operations.append(
                    UpdateOne(filter, {"$set": changes}, upsert=False)
                )
            try:
                if operations:
                    results = collection.bulk_write(operations)
                    print(
                        f"Documentos que coincidieron con el filtro modelID taxID: {results.matched_count}"
                    )
                    print(
                        f"Documentos modificados con éxito: {results.modified_count}"
                    )

            except PyMongoError as err:
                print(
                    "Algo salió mal al subir los documentos a la colección 'models'."
                    "Se van a restaurar los documentos modificados."
                )
                for doc in models_docs:
                    filter = {"modelID": doc["modelID"], "taxID": doc["taxID"]}
                    revert = {
                        key: value
                        for key, value in doc.items()
                        if key not in filter
                    }
                    rollback.append(
                        UpdateOne(filter, {"$set": revert}, upsert=False)
                    )

                results = collection.bulk_write(rollback)
                print(
                    f"Se hizo un rollback de: {results.modified_count} documentos en la colección 'models'."
                )
                print(f"⛔ Este fue el error: {err}")
                cnx.close()
                sys.exit(1)
            f.close()
        cnx.close()

    def models_stats(self, cnx):
        models_validation = True
        try:
            db = cnx[self.mongo_db]
            collection = db["models"]
            total_models = collection.count_documents({})
            active_models = collection.count_documents({ "isActive": True})
            published_models = collection.count_documents({ "isActive": True, "published": True})
            valid_models = collection.count_documents({ "isActive": True, "modelStatus": "Valid"})
            developing_models = collection.count_documents({ "isActive": True, "modelStatus": "Developing"})
            pendingValidation_models = collection.count_documents({ "isActive": True, "modelStatus": "pendingValidation"})
            
            data = [
                {"total": total_models},
                {"active": active_models},
                {"published": published_models},
                {"valid": valid_models},
                {"developing": developing_models},
                {"pendingValidation": pendingValidation_models},
            ]
            return data

        except OperationFailure as opfa:
            print(f"⛔ Error de operación en la base de datos MongoDB: {opfa}")
            sys.exit(1)