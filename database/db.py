import duckdb as dd
import os

worker_conn = None

def init_worker():
    global worker_conn
    
    worker_conn = dd.connect(f'/mnt/gdrive/data_aggregator_database_{os.getpid()}.db');

    # this is the unified value we actually want to achieve
    worker_conn.execute("""
    CREATE TABLE IF NOT EXISTS unified_books (
        title VARCHAR,
        author VARCHAR,
        main_category VARCHAR,
        rating HUGEINT,
        isbn VARCHAR,
    )
    """)