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
    def visit_huge_datasetbook(self, hugeDatasetBook: 'ingestors.HugeFirstDataset'):
        print("Cleaning huge dataset")
        pass