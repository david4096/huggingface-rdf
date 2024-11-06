import pytest
from unittest.mock import patch, MagicMock
from huggingface_rdf.fetch_data import croissant_dataset, get_datasets, fetch_datasets

@pytest.fixture
def mock_env_vars():
    with patch.dict('os.environ', {'HF_API_KEY': 'fake_api_key'}):
        yield

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {
        "name": "test_dataset",
        "description": "A test dataset"
    }
    return mock

def test_croissant_dataset(mock_env_vars, mock_response):
    with patch('requests.get', return_value=mock_response) as mock_get:
        result = croissant_dataset('test_dataset')
        
        mock_get.assert_called_once_with(
            "https://huggingface.co/api/datasets/test_dataset/croissant",
            headers={"Authorization": "Bearer fake_api_key"}
        )
        assert result == {"name": "test_dataset", "description": "A test dataset"}

def test_get_datasets(mock_env_vars):
    mock_dataset = MagicMock()
    mock_dataset.id = "test_dataset"
    
    with patch('huggingface_hub.list_datasets', return_value=[mock_dataset]) as mock_list:
        result = get_datasets(limit=1)
        
        mock_list.assert_called_once_with(limit=1)
        assert len(list(result)) == 1

def test_fetch_datasets(mock_env_vars, mock_response):
    mock_dataset = MagicMock()
    mock_dataset.id = "test_dataset"
    
    with patch('huggingface_rdf.fetch_data.get_datasets', return_value=[mock_dataset]) as mock_get:
        with patch('huggingface_rdf.fetch_data.croissant_dataset', return_value=mock_response.json()):
            result = fetch_datasets(limit=1)
            
            mock_get.assert_called_once_with(1)
            assert len(result) == 1
            assert result[0] == {"name": "test_dataset", "description": "A test dataset"}

def test_fetch_datasets_empty(mock_env_vars):
    with patch('huggingface_rdf.fetch_data.get_datasets', return_value=[]):
        result = fetch_datasets(limit=0)
        assert result == []
