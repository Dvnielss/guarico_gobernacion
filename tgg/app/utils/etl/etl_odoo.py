from .extraction.extract import Extractor
from .transformation.transform import Transformer
from .loading.loading import Loader



class ETL:
    def __init__(self):
        self.extractor = Extractor()
        self.transformer = Transformer()
        self.loader = Loader()

    def run_etl(self)-> None:
        data = self.extractor.extract_all_data()
        transformed_data = self.transformer.transform_all_data(data)
        self.loader.load_data(transformed_data)
