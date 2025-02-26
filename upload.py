from pathlib import Path 
from pecha_uploader.pipeline import upload
from pecha_uploader.config import Destination_url

from utils import read_json



input = read_json("jsons/chonjuk/commentary/I105531AD.json")
upload(input, Destination_url.STAGING, True)
