import os
import torch
from torch.utils.data import Dataset, DataLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))
DIR = os.path.join(PROJECT_ROOT, "data", "processed")

class FusionDataset(Dataset):

    def __init__(
            self,
            features_file: str,
            seed: int = 42
    ):
        self.features = torch.load(os.path.join(DIR, features_file))
        self.num_movies = self.features['text'].shape[0]

    def __len__(self):
        return self.num_movies

    def __getitem__(self, idx: int):
        return {
            'text': self.features['text'][idx],
            'keywords': self.features['keywords'][idx],
            'genres': self.features['genres'][idx],
            'poster_file': self.features['poster_file'][idx],
            'backdrop_file': self.features['backdrop_file'][idx],
            'year': self.features['year'][idx],
            'month_sin': self.features['month_sin'][idx],
            'month_cos': self.features['month_cos'][idx],
            'vote_average': self.features['vote_average'][idx],
            'vote_count': self.features['vote_count'][idx],
            'popularity': self.features['popularity'][idx],
            'runtime': self.features['runtime'][idx],
            'mask': self.features['mask'][idx]
        }

def get_dataloader(features_file, batch_size= 256, shuffle=True, num_workers=4, pin_memory=True, persistent_workers=True):
    ds = FusionDataset(features_file)

    return DataLoader(
            ds,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers,
            pin_memory=pin_memory,
            persistent_workers=persistent_workers,
            prefetch_factor=2
        )