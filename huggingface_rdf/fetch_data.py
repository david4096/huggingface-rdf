import requests
import os
from huggingface_hub import HfApi, list_datasets
from tqdm import tqdm

headers = {"Authorization": f"Bearer {os.environ['HF_API_KEY']}"}
API_URL = "https://huggingface.co/api/datasets/"

def croissant_dataset(dsid):
    response = requests.get(API_URL + dsid + "/croissant", headers=headers)
    return response.json()

def get_datasets(limit):
    return list(list_datasets(limit=limit))

def fetch_datasets(limit):
    datasets = get_datasets(limit)
    return [croissant_dataset(dataset.id) for dataset in tqdm(datasets, desc="Fetching datasets")]
