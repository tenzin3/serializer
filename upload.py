from pecha_uploader.pipeline import upload
from pecha_uploader.config import Destination_url

from utils import read_json

input = read_json("jsons/sherab/root/sherab_zh_translations.json")
upload(input, Destination_url.PRODUCTION, True)