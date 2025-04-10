from multiprocessing import Pool, cpu_count
from pacu.features.features import extract_features

import pandas as pd
import math
import sys

class FeatureExtractor:

    df: pd.DataFrame

    def __init__(self, path: str) -> None:
        self.df = pd.read_csv(path)


    def extract(self) -> None:

        n_procs = cpu_count()
        chunk_size = math.ceil(self.df.shape[0] / n_procs)
        chunks = []

        for i in range(n_procs):
            start_index = i * chunk_size
            end_index = (i + 1) * chunk_size
            df_chunk = self.df.iloc[start_index:end_index]
            chunks.append(df_chunk)

        with Pool(n_procs) as pool:
            results = pool.map(extract_features, chunks)
        
        self.df = pd.concat(results)


    def export(self, path: str) -> None:
        self.df.to_csv(path, index=False)
