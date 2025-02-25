from pathlib import Path 
from utils import download_pecha, write_json

from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.translation import TranslationSerializer

root_id = "I8BCEB363"
root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))
serialized = TranslationSerializer().serialize(root_pecha)
write_json("jsons/sherab/root/sherab_root.json", serialized)