from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from data_handlers.DataHandler import DataHandler
import pandas as pd
import numpy as np

if TYPE_CHECKING:
    import ingestors

class Cleaner(DataHandler):
    categorii_valide = ["Fiction", "Sci-Fi", "Mystery", "Biography", "History", "Fantasy", "Business", "Self-Help"]
    
    def visit_huge_datasetbook(self, processing_chunk):
        print("Visit huge datasetbook")
        pandas_frame = pd.DataFrame(processing_chunk);

        pandas_frame = pandas_frame.dropna()
        pandas_frame = pandas_frame[pandas_frame['category'].isin(self.categorii_valide)]
        pandas_frame = pandas_frame[pandas_frame['rating'] <= 5.00]

        print("end visiting")
        return pandas_frame;
