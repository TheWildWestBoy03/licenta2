class Transformer:
    def __init__(self, con):
        self.con = con

    def run(self):
        print("[TRANSFORM] starting final aggregation...")

        self.con.execute("""
            CREATE OR REPLACE TABLE unified_books AS
            SELECT
                isbn,
                title,
                ANY_VALUE(category) AS category,
                ANY_VALUE(author) AS author,
                AVG(rating) AS rating,
                COUNT(*) AS cnt
            FROM books_staging
            GROUP BY isbn, title
        """)

        print("[TRANSFORM] completed")