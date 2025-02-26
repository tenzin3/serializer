import io
import json 
import re 
import requests
import zipfile
import shutil

from pathlib import Path
from typing import Dict, List 

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

def parse_translated_sherab_commentary(content: Dict):
    segments = []
    for c in content:
        text = c["commentary"]
        text = normalize_escape_chars(text)
        text = remove_symbols(text)
        segments.append(text)
    return segments


def remove_symbols(text: str) -> str:
    """
    Remove hashtag
    """
    text = text.replace("#", "")
    return text

def normalize_escape_chars(text: str) -> str:
    text = text.replace('\"', "'").replace("\\/", "/")
    return text

def get_commentary_mapping(commentary_content: List[str]):
    mapping = []

    pattern = re.compile(r'(<\d+>)(<\d+>)')
    for content in commentary_content:
        match = pattern.search(content)
        if match:
            mapping.append(f"{match.group(1)}{match.group(2)}")
        else:
            mapping.append("")
    return mapping


if __name__ == "__main__":
    content = read_json("downloads/sherab/ai_commentaries/I22734F80_zh.json")
    commentary_translation = parse_translated_sherab_commentary(content)
    
    commentary_serialized = read_json("jsons/sherab/commentary/I22734F80.json")
    commentary_content = commentary_serialized["target"]["books"][0]["content"][0]
    mapping = get_commentary_mapping(commentary_content)

    mapped_translation = []
    for map, content in zip(mapping, commentary_translation):
        mapped_translation.append(f"{map}{content}")
    write_json("mapped_commentary.json", mapped_translation)