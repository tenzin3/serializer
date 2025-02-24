from pathlib import Path 
from utils import download_pecha, write_json

from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.translation import TranslationSerializer

root_id = "I5339F440"
root_pecha = Pecha.from_path(Path("tmp/I5339F440"))
serialized = TranslationSerializer().serialize(root_pecha)
write_json("jsons/sherab/root/pecha_display.json", serialized)