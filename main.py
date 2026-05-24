import ingestors
from data_handlers import Cleaner, Transformer, PipelineManager
from Cleaner
import pandas as pd

def main():
    pipeline = PipelineManager()
    ingestors_list = [ingestors.HugeFirstDataset()]
    data_processors = [data_handlers.Cleaner(), data_handlers.Transformer()]

    pipeline.add_step(data_processors[0])
    pipeline.add_step(data_processors[1])

    print("Starting etl pipeline...")

    # for ingestor in ingestors_list:
    #     ingestor.ingest(pipeline)

if __name__ == "__main__":
    main()