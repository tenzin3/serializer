from pathlib import Path 
from pecha_uploader.pipeline import upload
from pecha_uploader.config import Destination_url

from utils import read_json


dir_path = Path("jsons/chonjuk/commentary")

for json_file in dir_path.glob("*.json"):
    input = read_json(json_file)
    upload(input, Destination_url.PRODUCTION, True)
