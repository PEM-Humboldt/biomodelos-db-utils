import requests
from urllib.parse import quote_plus

import pandas as pd
from pymongo import MongoClient



class Mongo:
    def __init__(self, mongo_url=None, mongo_user=None, mongo_pass=None, mongo_db=None):
        if mongo_url and mongo_user and mongo_pass and mongo_db:
            [self.mongo_addr, self.mongo_port] = mongo_url.rsplit(':', 1)
            if not self.mongo_port:
                self.mongo_port = 27023
            else:
                self.mongo_port = int(self.mongo_port)
            self.mongo_user = mongo_user
            self.mongo_pass = mongo_pass
            self.mongo_db = 'produccion'
            self.mongo_url = mongo_url
            

    def query_mongo(self):
        mongo_url = f"mongodb://{quote_plus(self.mongo_user)}:{quote_plus(self.mongo_pass)}@{self.mongo_url}/?authMechanism=SCRAM-SHA-256&authSource={self.mongo_db}"
        cnx = MongoClient(mongo_url)
        db = cnx[self.mongo_db]
        collection = db["species"]
        
        # Example query to find a specific document
        prueba = collection.find({"species" : "Anthurium clavigerum"})
        cnx.close()
        
        return prueba