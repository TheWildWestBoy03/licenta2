from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import ingestors

class DataHandler(ABC):
    
    @abstractmethod
    def visit_huge_datasetbook(self, hugeDatasetBook: 'ingestors.HugeFirstDataset'):
        pass
