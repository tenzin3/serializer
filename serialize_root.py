from pathlib import Path 

from openpecha.pecha.serializers.pecha_db.root import RootSerializer
from openpecha.utils import write_json
from utils import download_pecha
from openpecha.pecha import Pecha 





root_display_id = "ID4931BF2"


root_display_pecha = Pecha.from_path(download_pecha(root_display_id, Path("tmp")))

work = RootSerializer()
json = work.serialize(root_display_pecha)

output_path = "jsons/dorjee/root"
write_json(f"{output_path}/{root_display_id}.json", json)
