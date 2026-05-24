from ingestors.Ingestor import Ingestor
from data_handlers.DataHandler import DataHandler
import pandas as pd
import os
from data_handlers.PipelineManager import PipelineManager

class HugeFirstDataset(Ingestor):
    def accept(self, data_handler : DataHandler):
        data_handler.visit_huge_datasetbook(self);
        pass

    def ingest(self, pipeline):
        print("Ingesting Huge Dataset")

        pipeline.execute_steps(self);
        pass