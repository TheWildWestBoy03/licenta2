import sys
import time

from ingestors.HugeFirstDataset import HugeFirstDataset
from data_handlers.PipelineManager import PipelineManager
from data_handlers.Cleaner import Cleaner
from data_handlers.DataLoader import DataLoader
from data_handlers.Transformer import Transformer


def build_pipeline():
    pipeline = PipelineManager()
    pipeline.add_step(Cleaner())
    return pipeline


def main():
    dataset_path = sys.argv[1]

    print("\n" + "=" * 80)
    print(f"[ETL START] dataset={dataset_path}")
    print("=" * 80)

    ingestor = HugeFirstDataset(dataset_path)
    pipeline = build_pipeline()
    loader = DataLoader()

    total_start = time.time()
    row_group_id = 0

    # 1. INGEST → CLEAN → LOAD
    for df in ingestor.stream():
        rg_start = time.time()

        print(f"\n[ROW_GROUP {row_group_id}] START")

        print(f"[ROW_GROUP {row_group_id}] INGESTED rows={len(df)}")

        t1 = time.time()
        cleaned = pipeline.execute(df)
        print(f"[ROW_GROUP {row_group_id}] CLEANED rows={len(cleaned)} time={time.time() - t1:.3f}s")

        t2 = time.time()
        loader.load(cleaned)
        print(f"[ROW_GROUP {row_group_id}] LOADED time={time.time() - t2:.3f}s")

        print(f"[ROW_GROUP {row_group_id}] DONE total_time={time.time() - rg_start:.3f}s")

        row_group_id += 1

    # 2. TRANSFORM
    print("\n[TRANSFORM] starting global aggregation...")

    transformer = Transformer(loader.con)

    t3 = time.time()
    transformer.run()
    print(f"[TRANSFORM] completed time={time.time() - t3:.3f}s")

    print("\n" + "=" * 80)
    print(f"[ETL DONE] total_time={time.time() - total_start:.3f}s")
    print("=" * 80)


if __name__ == "__main__":
    main()