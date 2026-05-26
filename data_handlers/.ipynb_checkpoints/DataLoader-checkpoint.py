import pandas as pd
from typing import TYPE_CHECKING, Dict
from data_handlers.DataHandler import DataHandler
import duckdb as dd
import database.db as database

if TYPE_CHECKING:
    import ingestors

class DataLoader(DataHandler):
    @property
    def con(self):
        return database.worker_conn
        
    def save_to_db(self, table_name: str, chunk: pd.DataFrame):
        if chunk is None:
            return
        
        if isinstance(chunk, pd.DataFrame) and chunk.empty:
            return
    
        self.con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM chunk WHERE 1=0")
        self.con.execute(f"INSERT INTO {table_name} SELECT * FROM chunk")
        print("Ceva");
        
    def visit_huge_datasetbook(self, hugeDatasetBook: 'ingestors.HugeFirstDataset', processing_chunk):
        self.save_to_db("huge_dataset_books", processing_chunk)
        
        return processing_chunk;