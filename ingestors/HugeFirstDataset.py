from ingestors.Ingestor import Ingestor
from data_handlers.DataHandler import DataHandler
from data_handlers.PipelineManager import PipelineManager

import os
import pandas as pd
import pyarrow.parquet as pa
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

_thread_local = threading.local()


def get_parquet(dataset_path):
    if not hasattr(_thread_local, "parquet_file"):
        _thread_local.parquet_file = pa.ParquetFile(dataset_path)
    return _thread_local.parquet_file


class HugeFirstDataset(Ingestor):
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    def process_batch(self, task_info):
        dataset_path, row_group_index, pipeline = task_info

        print(pipeline)
        print(f"Start row_group={row_group_index} pid={os.getpid()}")

        # parquet_file = get_parquet(dataset_path)
        # row_group_table = parquet_file.read_row_group(row_group_index)

        # df = row_group_table.to_pandas()


        start = time.time()
    
        parquet_file = get_parquet(self.dataset_path)
    
        t1 = time.time()
        row_group_table = parquet_file.read_row_group(row_group_index)
        print("READ TIME", time.time() - t1)
    
        t2 = time.time()
        df = row_group_table.to_pandas()
        print("PANDAS TIME", time.time() - t2)
    
        result = pipeline.execute_steps(self, df)

        print("TOTAL TIME", time.time() - start)
        print(f"Finish row_group={row_group_index} pid={os.getpid()}")

        return result

    def accept(self, data_handler: DataHandler, processing_chunk) -> pd.DataFrame:
        return data_handler.visit_huge_datasetbook(self, processing_chunk)

    def ingest(self, pipeline):
        num_threads = max(1, os.cpu_count() - 1)

        parquet_file = pa.ParquetFile(self.dataset_path)
        num_row_groups = parquet_file.num_row_groups

        tasks = [
            (self.dataset_path, i, pipeline)
            for i in range(num_row_groups)
        ]

        print(f"Running ETL with {num_threads} threads (ExecutorService)")

        results = []

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(self.process_batch, task)
                for task in tasks
            ]

            for future in as_completed(futures):
                results.append(future.result())

        return results