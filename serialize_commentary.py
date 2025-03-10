from pathlib import Path 

from openpecha.pecha.serializers.pecha_db.root import RootSerializer
from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary import PreAlignedCommentarySerializer
from openpecha.utils import write_json
from utils import download_pecha
from openpecha.pecha import Pecha 


root_display_id = "ID4931BF2"
root_id = "ID62D15D8"
prealigned_commentary_id = "IC4AB9E0B"

root_display_pecha = Pecha.from_path(download_pecha(root_display_id, Path("tmp")))
root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))
prealigned_commentary = Pecha.from_path(download_pecha(prealigned_commentary_id, Path("tmp")))

work = PreAlignedCommentarySerializer()
json = work.serialize(root_display_pecha, root_pecha, prealigned_commentary)

output_path = "jsons/dorjee/commentary"
write_json(f"{output_path}/{prealigned_commentary_id}.json", json)
