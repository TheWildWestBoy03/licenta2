import duckdb
import pandas as pd


class DataLoader:
    def __init__(self, db_path="data.db"):
        self.con = duckdb.connect(db_path)

        self.con.execute("""
            CREATE TABLE IF NOT EXISTS huge_dataset_books (
                title VARCHAR,
                author VARCHAR,
                category VARCHAR,
                rating DOUBLE,
                isbn VARCHAR
            )
        """)

    def save(self, df: pd.DataFrame):
        if df is None or df.empty:
            return

        # NO register (avoids shared state issues)
        self.con.execute(
            "INSERT INTO huge_dataset_books SELECT * FROM df",
            {"df": df}
        )

    def flush_many(self, dfs):
        self.con.execute("BEGIN TRANSACTION")

        for df in dfs:
            self.save(df)

        self.con.execute("COMMIT")