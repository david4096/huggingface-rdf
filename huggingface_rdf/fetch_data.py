import requests
import os
from huggingface_hub import HfApi, list_datasets
from tqdm import tqdm

headers = {"Authorization": f"Bearer {os.environ['HF_API_KEY']}"}
API_URL = "https://huggingface.co/api/datasets/"

def croissant_dataset(dsid):
    """
    Retrieves the 'croissant' metadata file for a specified dataset from Hugging Face.

    Args:
        dsid (str): The unique identifier of the dataset from which to retrieve the 'croissant' metadata file.

    Returns:
        dict: A JSON response containing metadata and details from the 'croissant' file for the specified dataset.
        
    """
    response = requests.get(API_URL + dsid + "/croissant", headers=headers)
    return response.json()

def get_datasets(limit):
    """
    Retrieves a list of datasets hosted on Hugging Face, up to the specified limit.

    Args:
        limit (int): The maximum number of datasets to retrieve.

    Returns:
        list: A list of dataset objects, each containing metadata for a Hugging Face dataset.
    """
    return list(list_datasets(limit=limit))

def fetch_datasets(limit):
    """
    Fetches metadata for multiple datasets from Hugging Face, including the 'croissant' metadata file for each.

    This is a wrapper function that retrieves a limited list of datasets using `get_datasets` 
    and then fetches the 'croissant' metadata for each dataset.

    Args:
        limit (int): The maximum number of datasets to retrieve and process.

    Returns:
        list: A list of dictionaries, each containing the 'croissant' metadata for a dataset.
    """
    datasets = get_datasets(limit)
    return [croissant_dataset(dataset.id) for dataset in tqdm(datasets, desc="Fetching datasets")]
