import pyarrow.parquet as pa

class HugeFirstDataset:
    def __init__(self, path):
        self.path = path

    def stream(self):
        parquet = pa.ParquetFile(self.path)

        for i in range(parquet.num_row_groups):
            yield parquet.read_row_group(i).to_pandas()