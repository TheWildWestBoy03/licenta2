import pandas as pd
from typing import TYPE_CHECKING, Dict
from data_handlers.DataHandler import DataHandler
import database.db as database

if TYPE_CHECKING:
    import ingestors

class Transformer(DataHandler):
    @property
    def con(self):
        return database.worker_conn

    def save_to_db(self, final_df):
        if not isinstance(chunk, pd.DataFrame):
            print(f"⚠️ Warning: Received empty DataFrame for table {table_name} not actual Data Frame. Skipping.")
            return
            
        if isinstance(chunk, pd.DataFrame) and chunk.empty:
            print(f"⚠️ Warning: Received empty DataFrame for table {table_name}. Skipping.")
            return

        self.con.execute(f"""
            INSERT INTO unified_books AS SELECT * FROM final_df
        """)
        
    def visit_huge_datasetbook(self, hugeDatasetBook: 'ingestors.HugeFirstDataset', processing_chunk):
        resulted_df = self.con.execute("""
            SELECT
                book_id as isbn,
                title,
                category as main_category,
                rating,
                author
            FROM processing_chunk                
        """);
        
        resulted_df = save_to_db(resulted_df);
                                 
        pass