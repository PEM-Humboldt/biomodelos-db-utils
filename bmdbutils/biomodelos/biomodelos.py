import requests
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine


class Biomodelos:
    def __init__(
        self,
        api_url=None,
        pg_url=None,
        pg_user=None,
        pg_pass=None,
    ):
        self.api_url = api_url
        if pg_url and pg_user and pg_pass:
            [self.pg_addr, self.pg_port] = pg_url.rsplit(":", 1)
            if not self.pg_port:
                self.pg_port = 5430
            else:
                self.pg_port = int(self.pg_port)
            self.pg_user = pg_user
            self.pg_pass = pg_pass
            self.pg_db = "biomodelos_pro"

    def update_model_layer(self, model_id, layer):
        r = requests.put(
            f"{self.api_url}/tools/models/{model_id}/layer",
            data={"layer_name": layer},
        )

    def query_ratings(self, tax_ids, init_date, end_date):
        cnx = create_engine(
            "postgresql://{username}:{password}@{addr}:{port}/{dbname}".format(
                username=self.pg_user,
                password=quote_plus(self.pg_pass),
                addr=self.pg_addr,
                port=self.pg_port,
                dbname=self.pg_db,
            )
        )
        query = """SELECT rt.user_id, u.name, rt.model_id, rt.species_id, s.accepted_name, rt.score
            FROM ratings as rt
            JOIN users as u ON u.id = rt.user_id
            JOIN species as s ON s.species_id = rt.species_id
            WHERE rt.updated_at > '{init_date}'
            AND rt.updated_at <= '{end_date}'
            AND rt.species_id IN ({tax_ids})
            """.format(
            init_date=init_date, end_date=end_date, tax_ids=",".join(tax_ids)
        )
        ratings = pd.read_sql_query(query, cnx)
        return ratings

    def query_editions(self, tax_ids, init_date, end_date):
        cnx = create_engine(
            "postgresql://{username}:{password}@{addr}:{port}/{dbname}".format(
                username=self.pg_user,
                password=quote_plus(self.pg_pass),
                addr=self.pg_addr,
                port=self.pg_port,
                dbname=self.pg_db,
            )
        )
        query = """SELECT ul.user_id, u.name, ul.species_id, ul."newModel", ul.threshold, ul.final, ul."geoJSON", ul.created_at, ul.updated_at
            FROM users_layers AS ul
            JOIN users AS u ON u.id = ul.user_id
            WHERE ul.updated_at > '{init_date}'
            AND ul.updated_at <= '{end_date}'
            AND ul.species_id IN ({tax_ids})
            """.format(
            init_date=init_date, end_date=end_date, tax_ids=",".join(tax_ids)
        )
        editions = pd.read_sql_query(query, cnx)
        return editions

    def query_ecovars(self, tax_ids, init_date, end_date):
        cnx = create_engine(
            "postgresql://{username}:{password}@{addr}:{port}/{dbname}".format(
                username=self.pg_user,
                password=quote_plus(self.pg_pass),
                addr=self.pg_addr,
                port=self.pg_port,
                dbname=self.pg_db,
            )
        )
        query = """SELECT evs.user_id, u.name, evs.species_id, ev.name ecological_variable, evs.created_at, evs.updated_at
            FROM eco_variables_species AS evs
            JOIN users AS u ON u.id = evs.user_id
            JOIN eco_variables AS ev ON ev.id = evs.eco_variable_id
            WHERE evs.updated_at > '{init_date}'
            AND evs.updated_at <= '{end_date}'
            AND evs.species_id IN ({tax_ids})
            """.format(
            init_date=init_date, end_date=end_date, tax_ids=",".join(tax_ids)
        )
        ecovars = pd.read_sql_query(query, cnx)
        return ecovars
    
    def query_users(self):
        cnx = create_engine(
            "postgresql://{username}:{password}@{addr}:{port}/{dbname}".format(
                username=self.pg_user,
                password=quote_plus(self.pg_pass),
                addr=self.pg_addr,
                port=self.pg_port,
                dbname=self.pg_db,
            )
        )
        query = """SELECT COUNT(*) AS total_users
                FROM users
                """
        total_users = pd.read_sql_query(query, cnx)

        query = """SELECT COUNT(expertise) AS total_expertise
                FROM users
                WHERE expertise IS NOT NULL
                AND trim(expertise) <> ''
                """
        expertise_users = pd.read_sql_query(query, cnx)

        
        return total_users, expertise_users

    def query_downloads(self):
        cnx = create_engine(
            "postgresql://{username}:{password}@{addr}:{port}/{dbname}".format(
                username=self.pg_user,
                password=quote_plus(self.pg_pass),
                addr=self.pg_addr,
                port=self.pg_port,
                dbname=self.pg_db,
            )
        )
        query = """SELECT COUNT (*) as total_downloads, m.description
                    FROM downloads AS d
                    JOIN model_uses AS m ON d.model_use_id = m.id
                    group by m.description
                """
        downloads = pd.read_sql_query(query, cnx)
       
        return downloads

    def query_groups(self):
        cnx = create_engine(
            "postgresql://{username}:{password}@{addr}:{port}/{dbname}".format(
                username=self.pg_user,
                password=quote_plus(self.pg_pass),
                addr=self.pg_addr,
                port=self.pg_port,
                dbname=self.pg_db,
            )
        )
        query = """SELECT DISTINCT COUNT (*) AS total_groups
                FROM groups
                """
        total_groups = pd.read_sql_query(query, cnx)
        query = """SELECT DISTINCT COUNT (*) AS active_groups
                FROM groups g
                WHERE g.group_state_id = 1
                """
        active_groups = pd.read_sql_query(query, cnx)
                
        return total_groups, active_groups