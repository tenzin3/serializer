from pathlib import Path 

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.root import RootSerializer
from openpecha.utils import write_json
from utils import download_pecha

translation_pecha = Pecha.from_path(download_pecha("I542210F9", Path("tmp")))
root_pecha = Pecha.from_path(download_pecha("I5339F440", Path("tmp")))


serializer = RootSerializer()
json = serializer.serialize(translation_pecha, root_pecha)
write_json("new.json", json)