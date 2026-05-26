import ingestors
from data_handlers.Cleaner import Cleaner
from data_handlers.Transformer import Transformer
from data_handlers.PipelineManager import PipelineManager
from data_handlers.DataLoader import DataLoader
import pandas as pd
import sys

def main():
    dataset_path = sys.argv[1]

    print(dataset_path);
    pipeline = PipelineManager()
    ingestors_list = [ingestors.HugeFirstDataset(dataset_path)]
    data_processors = [Cleaner(), DataLoader(), Transformer()]

    pipeline.add_step(data_processors[0])
    pipeline.add_step(data_processors[1])
    pipeline.add_step(data_processors[2])

    print("Starting etl pipeline...")

    for ingestor in ingestors_list:
        ingestor.ingest(pipeline)

if __name__ == "__main__":
    main()