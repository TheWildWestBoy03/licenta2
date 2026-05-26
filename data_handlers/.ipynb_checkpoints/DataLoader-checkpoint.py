import duckdb
import pandas as pd

class DataLoader:
    def __init__(self, db_path="/mnt/gdrive/data.db"):
        self.con = duckdb.connect(db_path)

        self.con.execute("""
            CREATE TABLE IF NOT EXISTS books_staging (
                isbn VARCHAR,
                title VARCHAR,
                category VARCHAR,
                rating DOUBLE,
                author VARCHAR
            )
        """)

    def load(self, df: pd.DataFrame):
        if df is None or df.empty:
            return

        self.con.register("chunk", df)

        self.con.execute("""
            INSERT INTO books_staging
            SELECT * FROM chunk
        """)