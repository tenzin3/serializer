from pathlib import Path 

from openpecha.pecha.serializers.pecha_db.root import RootSerializer
from openpecha.pecha.serializers.pecha_db.prealigned_root_translation import PreAlignedRootTranslationSerializer
from openpecha.utils import write_json
from utils import download_pecha
from openpecha.pecha import Pecha 
from work_ids.dorjee import works




root_display_id = "ID4931BF2"
root_id = "I665430B4"
translation_id = "IF915B644"
    
root_display_pecha = Pecha.from_path(download_pecha(root_display_id, Path("tmp")))
root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))
translation_pecha = Pecha.from_path(download_pecha(translation_id, Path("tmp")))

work = PreAlignedRootTranslationSerializer()
json = work.serialize(root_display_pecha, root_pecha, translation_pecha)

write_json(f"new.json", json)
