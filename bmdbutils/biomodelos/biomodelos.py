import requests
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine


class Biomodelos:
    def __init__(self, api_url=None, pg_url=None, pg_user=None, pg_pass=None):
        self.api_url = api_url
        if pg_url and pg_user and pg_pass:
            [self.pg_addr, self.pg_port] = pg_url.rsplit(':', 1)
            if not self.pg_port:
                self.pg_port = 5432
            else:
                self.pg_port = int(self.pg_port)
            self.pg_user = pg_user
            self.pg_pass = pg_pass
            self.pg_db = 'biomodelos_pro'

    def update_model_layer(self, model_id, layer):
        r = requests.put(
            f"{self.api_url}/tools/models/{model_id}/layer", data={"layer_name": layer}
        )

    def query_ratings(self, tax_ids, init_date, end_date):
        cnx = create_engine('postgresql://{username}:{password}@{addr}:{port}/{dbname}'.format(
            username=self.pg_user, password=quote_plus(self.pg_pass), addr=self.pg_addr, port=self.pg_port, dbname=self.pg_db))
        query = """SELECT user_id, model_id, species_id, score
            FROM ratings
            WHERE created_at > '{init_date}'
            AND created_at <= '{end_date}'
            AND species_id IN ({tax_ids})
            """.format(init_date=init_date, end_date=end_date, tax_ids=",".join(tax_ids))
        ratings = pd.read_sql_query(query, cnx)
        return ratings
