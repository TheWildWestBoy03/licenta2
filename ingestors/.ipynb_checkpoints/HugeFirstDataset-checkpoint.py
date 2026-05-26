from ingestors.Ingestor import Ingestor
from data_handlers.DataHandler import DataHandler
import pandas as pd
import os
from data_handlers.PipelineManager import PipelineManager
import multiprocessing as mp
import pyarrow.parquet as pa
import duckdb as dd
import database.db as database

class HugeFirstDataset(Ingestor):
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path;

    def process_batch(self, task_info):
        dataset_path, row_group_index, pipeline_steps = task_info

        parquet_file = pa.ParquetFile(dataset_path)
        row_group_table = parquet_file.read_row_group(row_group_index)

        local_pipeline = PipelineManager()
        for step in pipeline_steps:
            local_pipeline.add_step(step)
            
        local_pipeline.execute_steps(self, row_group_table.to_pandas());
        pass

    def accept(self, data_handler : DataHandler, processing_chunk) -> pd.DataFrame :
        return data_handler.visit_huge_datasetbook(self, processing_chunk);

    def ingest(self, pipeline):
        print("Ingesting Huge Dataset")

        num_cores = max(1, mp.cpu_count() - 1)
        parquet_file = pa.ParquetFile(self.dataset_path);
        num_row_groups = parquet_file.num_row_groups;
        tasks = [(self.dataset_path, i, pipeline.steps) for i in range(num_row_groups)];

        print(num_row_groups);
        
        with mp.Pool(processes=num_cores, initializer=database.init_worker) as pool:
            pool.map(self.process_batch, tasks)

        pass