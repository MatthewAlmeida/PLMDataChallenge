"""
This file implements function load_to_sql,
which loads the raw data from the provided
csv files using pandas and populates tables in
the postgres database defined in 
the docker-compose with that data.
"""

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


data_manifest = {
    "alsfrs": "./raw/user_ALSFRS_score.csv",
    "condition": "./raw/user_condition.csv",
    "onset": "./raw/user_onset_date.csv",
    "symptom": "./raw/user_symptom.csv"
}

def populate_postgres():
    # Populate environment variables; these
    # are also used in the docker-compose to 
    # create the postgres container
    load_dotenv(find_dotenv())

    # Collect connection parameters from environment vars
    pg_user = os.environ["POSTGRES_USERNAME"]
    pg_password = os.environ["POSTGRES_PASSWORD"]
    pg_host = os.environ["POSTGRES_HOST"]
    pg_database = os.environ["POSTGRES_DATABASE"]

    # Build connection string
    connection_string = (
        f"postgresql+psycopg2://"
        f"{pg_user}:{pg_password}@localhost:5432/{pg_database}"
    )

    # Start engine
    engine = create_engine(connection_string)

    # Loop through the data manifest and create the tables
    for table_name, file_path in data_manifest.items():
        print(f"Loading from csv file: {file_path}")

        # Read in the data
        table_df = pd.read_csv(file_path)
        
        print(f"  ...loaded {len(table_df)} rows.")
        print(f"Creating SQL table.")

        start_time = time.time()

        # Load in the table    
        table_df.to_sql(
            table_name,
            con=engine,
            if_exists="replace",
            schema="public" # Process will silently fail if schema not included.
            # Postgres uses this schema name more like a namespace than 
            # a traditional schema; default is "public".
        )

        end_time = time.time()

        print(f"  ...done in {end_time-start_time:.0f}s")

if __name__ == "__main__":
    populate_postgres()
