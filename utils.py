import io
import json 
import requests
import zipfile
import shutil

from pathlib import Path
from typing import Dict 

def read_json(file_path):
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_pecha_metadata(pecha_id: str) -> Dict:
    # Construct the URL
    url = f'https://api-aq25662yyq-uc.a.run.app/metadata/{pecha_id}'
    
    # Set the headers
    headers = {
        'accept': 'application/json'
    }
    
    # Send the GET request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response and return it as a dictionary
        return response.json()
    else:
        raise Exception(f"Failed to fetch metadata. Status code: {response.status_code}")


def download_pecha(pecha_id: str, output_path: Path) -> Path:
    url = f'https://api-aq25662yyq-uc.a.run.app/pecha/{pecha_id}'
    
    headers = {
        'accept': 'application/zip'
    }
    response = requests.get(url, headers=headers, stream=True)
    
    if response.status_code == 200:
        extracted_folder_name = f"{pecha_id}"
        extracted_folder_path = output_path / pecha_id
        
        if extracted_folder_path.exists():
            shutil.rmtree(extracted_folder_path)  

        extracted_folder_path.mkdir(parents=True, exist_ok=True)
        
        with io.BytesIO(response.content) as zip_buffer:
            with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
                zip_ref.extractall(extracted_folder_path)
        
        return extracted_folder_path
    else:
        raise Exception(f"Failed to download pecha. Status code: {response.status_code}")

if __name__ == "__main__":
    pecha_id = "I22734F80"
    pecha_path = download_pecha(pecha_id, Path("."))
    print(pecha_path)