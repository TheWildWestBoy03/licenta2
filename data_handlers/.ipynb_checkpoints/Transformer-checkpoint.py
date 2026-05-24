import pandas as pd
from typing import TYPE_CHECKING, Dict
from data_handlers.DataHandler import DataHandler

if TYPE_CHECKING:
    import ingestors

class Transformer(DataHandler):
    def visit_huge_datasetbook(self, hugeDatasetBook: 'ingestors.HugeFirstDataset'):
        print("Transforming huge dataset")

        pass