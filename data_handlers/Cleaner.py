from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from data_handlers.DataHandler import DataHandler
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency

if TYPE_CHECKING:
    import ingestors

class Cleaner(DataHandler):
    categorii_valide = ["Fiction", "Sci-Fi", "Mystery", "Biography", "History", "Fantasy", "Business", "Self-Help"]
    
    def visit_huge_datasetbook(self, hugeDatasetBook: 'ingestors.HugeFirstDataset', processing_chunk):
        pandas_frame = pd.DataFrame(processing_chunk);

        print("Before: ", sep=' ');
        print(pandas_frame.shape);

        pandas_frame = pandas_frame.dropna()
        pandas_frame = pandas_frame[pandas_frame['category'].isin(self.categorii_valide)]
        pandas_frame = pandas_frame[pandas_frame['rating'] <= 5.00]

        print("After: ", sep=' ');
        print(pandas_frame.shape);
        
        return pandas_frame;
