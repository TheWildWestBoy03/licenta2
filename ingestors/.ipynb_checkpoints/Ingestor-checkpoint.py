from abc import ABC, abstractmethod
from data_handlers.DataHandler import DataHandler

class Ingestor(ABC):
    @abstractmethod
    def accept(self, data_handler : DataHandler):
        pass
    
    @abstractmethod
    def ingest(self):
        pass