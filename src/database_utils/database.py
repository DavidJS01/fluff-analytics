import psycopg2
import os
from database_utils.queries import EXAMPLE_SELECT_SUMMONERS


def create_postgres_conn() -> psycopg2.connect.__class__:
    try:
        conn = psycopg2.connect(
            user="postgres",
            password=os.getenv("SUPABASE_DB_PASSWORD"),
            host=os.getenv("SUPABASE_DB_HOST"),
            port=5432,
            database="postgres",
        )
        return conn
    except Exception as e:
        raise e


def example_execute_query() -> list:
    try:
        conn = create_postgres_conn()  # create a connection to the postgres database
        cursor = conn.cursor()  # create a cursor that lets us run queries
        cursor.execute(
            EXAMPLE_SELECT_SUMMONERS
        )  # run the `EXAMPLE_SELECT_SUMMONERS query`
        data = cursor.fetchall()  # access the data that is now stored in the cursor
        return data
    except Exception as e:
        raise e
