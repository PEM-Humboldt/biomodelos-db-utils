import json
import pandas as pd
import sys
from datetime import datetime
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

    def validate_date_fields(self, csv_file):
        try:
            df = pd.read_csv(csv_file)
            today = datetime.now()
            current_year = today.year
            current_month = today.month
            current_day = today.day
            invalid_rows = []

            for idx, row in df.iterrows():
                year = row.get('year')
                month = row.get('month')
                day = row.get('day')

                # Si no hay ninguno, saltar
                if pd.isna(year) and pd.isna(month) and pd.isna(day):
                    continue

                # Compara cada campo existente
                if pd.notna(year) and int(year) > current_year:
                    invalid_rows.append((idx, f"Año inválido: {year} > {current_year}"))
                    continue

                if pd.notna(month):
                    if pd.isna(year) or int(year) == current_year:  # compara mes solo si aplica
                        if int(month) > current_month:
                            invalid_rows.append((idx, f"Mes inválido: {month} > {current_month}"))
                            continue

                if pd.notna(day):
                    if (pd.isna(year) or int(year) == current_year) and (pd.isna(month) or int(month) == current_month):
                        if int(day) > current_day:
                            invalid_rows.append((idx, f"Día inválido: {day} > {current_day}"))

            if invalid_rows:
                print("❌ Fechas inválidas encontradas:")
                for idx, msg in invalid_rows:
                    print(f"  - Fila {idx + 1}: {msg}")
                return False
            else:
                print("✅ Las columnas tienen fechas válidas o anteriores a hoy.")
                return True

        except Exception as e:
            print(f"⛔ Error al validar el archivo '{csv_file}': {e}")
            return False

    def validate_csv_data(self, csv_file, collection):
        config = {
            "records": (
                "tmp/records_output.json",
                "bmdbutils/biomodelos/schemas/records.json",
                "tmp/records_error.txt",
            ),
            "models_metadata": (
                "tmp/metadata_output.json",
                "bmdbutils/biomodelos/schemas/models_metadata.json",
                "tmp/metadata_error.txt",
            ),
        }
        jsonFile, schemaFile, outputErrorFile = config[collection]
        try:
            df_file = pd.read_csv(csv_file)
            df_file.to_json(jsonFile, orient="records", lines=True)
            with open(schemaFile, "r") as f:
                schema = json.load(f)
                validator = Draft7Validator(
                    schema, format_checker=FormatChecker()
                )
                f.close()
            with open(jsonFile, "r") as f:
                data = [json.loads(line) for line in f]
                f.close()
            with open(outputErrorFile, "w") as f:
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

        with open("tmp/records_output.json", "r") as f:
            data = [json.loads(line) for line in f]
            f.close()
        try:
            with open("tmp/records_uploaded.txt", "w") as f:
                for record in data:
                    record["createdDate"] = pd.Timestamp.now().isoformat()
                    inserted_record = collection.insert_one(record)
                    inserted_list.append(inserted_record.inserted_id)
                    f.write(
                        f"Documento con _id: {inserted_record.inserted_id} cargado correctamente a la colección 'records'.\n"
                    )
            f.close()
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
            f"""✅ Se subieron {len(data)} documentos a la colección 'records'. 
El archivo records_uploaded.txt tiene los ids que se cargaron a la colección. 
Busca este archivo en la ruta ./tmp/"""
        )
        cnx.close()

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

    def update_models_metadata(self, models_docs, cnx):
        db = cnx[self.mongo_db]
        collection = db["models"]
        operations = []
        rollback = []
        with open("tmp/metadata_output.json", "r") as f:
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
            total_models = collection.count_documents({"isActive": True})
            published_models = collection.count_documents(
                {
                    "isActive": True,
                    "published": True,
                    "modelStatus": "pendingValidation",
                }
            )
            valid_models = collection.count_documents(
                {"isActive": True, "modelStatus": "Valid"}
            )
            developing_models = collection.count_documents(
                {
                    "isActive": True,
                    "published": False,
                    "modelStatus": "pendingValidation",
                }
            )
            statistics_models = collection.count_documents(
                {"isActive": True, "modelStatus": "Statistic"}
            )

            data = [
                {"Totales": total_models},
                {"Publicados": published_models},
                {"Validados": valid_models},
                {"en Desarrollo": developing_models},
                {"Estadísticos": statistics_models},
            ]
            return data

        except OperationFailure as opfa:
            print(f"⛔ Error de operación en la base de datos MongoDB: {opfa}")
            sys.exit(1)
