from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    import ingestors

class DataHandler(ABC):
    
    @abstractmethod
    def visit_huge_datasetbook(self, hugeDatasetBook: 'ingestors.HugeFirstDataset', processing_chunk):
        pass
