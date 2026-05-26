import os
import pyarrow.parquet as pa
import threading
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

_thread_local = threading.local()


def get_parquet(path):
    """
    Thread-local Parquet cache (safe, but we are NOT using threads anymore).
    Kept for future extension.
    """
    if not hasattr(_thread_local, "pf"):
        _thread_local.pf = pa.ParquetFile(path)
    return _thread_local.pf


class HugeFirstDataset:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    # ----------------------------
    # SINGLE WORKER (NO THREADS)
    # ----------------------------
    def process_batch(self, parquet, row_group_index, pipeline):
        start = time.time()

        logging.info(f"[START] row_group={row_group_index}")

        # READ ROW GROUP (one at a time → no memory explosion)
        t0 = time.time()
        row_group = parquet.read_row_group(row_group_index)
        logging.info(f"[READ] row_group={row_group_index} {time.time() - t0:.3f}s")

        # CONVERT TO PANDAS (ONLY ONE AT A TIME)
        t1 = time.time()
        df = row_group.to_pandas()
        logging.info(f"[PANDAS] row_group={row_group_index} rows={len(df)} {time.time() - t1:.3f}s")

        # PIPELINE EXECUTION (PURE COMPUTE)
        t2 = time.time()
        result = pipeline.execute_steps(df)
        logging.info(f"[PIPELINE] row_group={row_group_index} {time.time() - t2:.3f}s")

        logging.info(f"[FINISH] row_group={row_group_index} TOTAL={time.time() - start:.3f}s")

        return result

    # ----------------------------
    # SAFE INGESTION (SEQUENTIAL)
    # ----------------------------
    def ingest(self, pipeline):
        parquet = pa.ParquetFile(self.dataset_path)
        num_row_groups = parquet.num_row_groups

        logging.info(f"[INGEST START] row_groups={num_row_groups}")

        results = []

        for i in range(num_row_groups):
            result = self.process_batch(parquet, i, pipeline)
            results.append(result)

            logging.info(f"[PROGRESS] {i + 1}/{num_row_groups}")

        logging.info("[INGEST DONE]")

        return results