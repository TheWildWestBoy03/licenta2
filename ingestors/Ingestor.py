from abc import ABC, abstractmethod
from data_handlers.DataHandler import DataHandler
import pandas as pd

class Ingestor(ABC):
    @abstractmethod
    def accept(self, data_handler : DataHandler, processing_chunk) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def ingest(self):
        pass