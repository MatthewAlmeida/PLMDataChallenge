"""
This file implements the backend of the dashboard
as a Backend class that handles the connections to
the database by providing a wrapper function for 
each query that can be used by the components
in PLMDashComponents.
"""

import numpy as np
import os
import pandas as pd
import psycopg2
import time

from dotenv import (
    find_dotenv,
    load_dotenv
)
from pathlib import Path
from sqlalchemy import create_engine

class Backend(object):
    def __init__(self, use_docker_host=True):
        load_dotenv(find_dotenv())
        self.pg_user = os.environ["POSTGRES_USERNAME"]
        self.pg_password = os.environ["POSTGRES_PASSWORD"]
        self.pg_database = os.environ["POSTGRES_DATABASE"]
        self.pg_host = os.environ["POSTGRES_HOST"] if use_docker_host else "localhost"

        self.connection_string = (
            f"postgresql+psycopg2://"
            f"{self.pg_user}:{self.pg_password}@{self.pg_host}:5432/{self.pg_database}"
        )
        
        self.db_engine = create_engine(self.connection_string)


    # This function does the heavy lifting; given 
    # query text, gets a connection from the sqlalchemy
    # engine and hits the database with it;

    def _get_pandas_result_set(self, query, **kwargs):
        with self.db_engine.connect() as connection:
            result_set = pd.read_sql(query, connection, **kwargs)
        
        return result_set

    def get_condition_card_data(self):
        query = """
            SELECT c.condition_name, COUNT(c.condition_name) AS Users
            FROM (SELECT DISTINCT user_id FROM alsfrs) AS a
                INNER JOIN condition c ON a.user_id = c.user_id
            GROUP BY c.condition_name
            ORDER BY Users desc;
        """

        return self._get_pandas_result_set(query)

    def get_users_from_alsfrs_onset(self):
        query = """
            SELECT DISTINCT a.user_id 
            FROM alsfrs a INNER JOIN onset o
            ON a.user_id = o.user_id;
        """

        return self._get_pandas_result_set(query)

    def get_alsfrs_series_by_user_id(self, user_id):
        query = f"""
            SELECT a.user_id, a.report_date, a.score
            FROM alsfrs a
            WHERE a.user_id = {user_id}
            ORDER BY a.report_date;
        """

        rs = self._get_pandas_result_set(query)
        rs["report_date"] = pd.to_datetime(rs["report_date"])

        return rs

    def get_alsfrs_min_date_by_user(self):
        query = f"""
            SELECT a.user_id, MIN(a.report_date) as min_date
            FROM alsfrs a
            GROUP BY a.user_id;
        """

        rs = self._get_pandas_result_set(query)
        rs["min_date"] = pd.to_datetime(rs["min_date"])

        return rs

    def get_alsfrs_table_by_user_set(self, users):
        # Ugly line of code, but trims what we
        # need out of the numpy array repr string
        users = np.array(users).flatten()

        user_str = f"({users.__repr__()[7:-2]})"

        query = f"""
            SELECT a.user_id, a.report_date, a.score
            FROM alsfrs a
            WHERE a.user_id IN {user_str}
            ORDER BY a.report_date;
        """

        rs = self._get_pandas_result_set(query)
        rs["report_date"] = pd.to_datetime(rs["report_date"])

        return rs

    def get_normalized_alsfrs_series_random_users(self, n_random_users):
        # Get the users that are in both alsfrs and onsetusers = self.get_users_from_alsfrs_onset()

        users = self.get_users_from_alsfrs_onset()

        # select n_random_users of them
        selected_users = np.random.permutation(users)[:n_random_users]

        # Get the minimum date by user
        min_by_user = self.get_alsfrs_min_date_by_user()

        # Get the alsfrs data
        alsfrs = self.get_alsfrs_table_by_user_set(selected_users)

        # Convert to ordinal (Days after first report date)
        alsfrs["report_date"] = alsfrs.report_date.apply(lambda x: x.toordinal())
        min_by_user["min_date"] = min_by_user.min_date.apply(lambda x: x.toordinal())

        alsfrs_w_min = alsfrs.merge(min_by_user, on="user_id")

        alsfrs_w_min["days_since_first_report"] = alsfrs_w_min.report_date - alsfrs_w_min.min_date

        return alsfrs_w_min



