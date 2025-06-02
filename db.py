import psycopg2
import pandas as pd

# Database connection settings
DB_HOST = "localhost"
DB_NAME = "food_management_db"
DB_USER = "postgres"
DB_PASSWORD = "guvi"

# Establish a connection to the PostgreSQL database
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Run any SQL query (SELECT, INSERT, UPDATE, DELETE)
def run_query(query, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if query.strip().lower().startswith("select"):
                cols = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return [dict(zip(cols, row)) for row in rows]
            else:
                conn.commit()
                return None

# Load full table as a DataFrame (for display)
def load_table_data(table_name):
    with get_connection() as conn:
        df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    return df
