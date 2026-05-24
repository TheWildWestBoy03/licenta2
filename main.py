import ingestors
from data_handlers.Cleaner import Cleaner
from data_handlers.Transformer import Transformer
from data_handlers.PipelineManager import PipelineManager
import pandas as pd

def main():
    pipeline = PipelineManager()
    ingestors_list = [ingestors.HugeFirstDataset()]
    data_processors = [Cleaner(), Transformer()]

    pipeline.add_step(data_processors[0])
    pipeline.add_step(data_processors[1])

    print("Starting etl pipeline...")

    for ingestor in ingestors_list:
        ingestor.ingest(pipeline)

if __name__ == "__main__":
    main()