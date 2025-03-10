from pathlib import Path 

from openpecha.pecha.serializers.pecha_db.root import RootSerializer
from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary import PreAlignedCommentarySerializer
from openpecha.utils import write_json
from utils import download_pecha
from openpecha.pecha import Pecha 
from work_ids.dorjee import works

for work_id in works:
    root_display_id = work_id["root_display_id"]
    root_id = work_id["root_id"]
    commentary_id = work_id["commentary_id"]
        
    root_display_pecha = Pecha.from_path(download_pecha(root_display_id, Path("tmp")))
    root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))
    prealigned_commentary = Pecha.from_path(download_pecha(commentary_id, Path("tmp")))

    work = PreAlignedCommentarySerializer()
    json = work.serialize(root_display_pecha, root_pecha, prealigned_commentary)

    output_path = "jsons/dorjee/commentary"
    write_json(f"{output_path}/{commentary_id}.json", json)
