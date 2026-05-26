import sys

from ingestors.HugeFirstDataset import HugeFirstDataset
from data_handlers.PipelineManager import PipelineManager
from data_handlers.Cleaner import Cleaner
from data_handlers.DataLoader import DataLoader


def build_pipeline():
    pipeline = PipelineManager()

    # STAGE: CLEANING / TRANSFORM LOGIC ONLY
    pipeline.add_step(Cleaner())

    return pipeline


def main():
    dataset_path = sys.argv[1]

    print(f"Starting ELT pipeline for: {dataset_path}")

    pipeline = build_pipeline()

    ingestor = HugeFirstDataset(dataset_path)

    print("Running parallel compute stage...")
    results = ingestor.ingest(pipeline)

    print(f"Compute stage finished. Processed {len(results)} chunks.")

    print("Writing to DuckDB...")

    loader = DataLoader()
    loader.flush_many(results)

    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()