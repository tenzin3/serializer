import json 
import requests

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
    

if __name__ == "__main__":
    pecha_id = "I22734F80"
    metadata = get_pecha_metadata(pecha_id)
    print(metadata)