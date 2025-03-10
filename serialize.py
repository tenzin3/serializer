from pathlib import Path 

from openpecha.pecha.serializers.pecha_db.root import RootSerializer
from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary import PreAlignedCommentarySerializer
from openpecha.utils import write_json
from utils import download_pecha
from openpecha.pecha import Pecha 

root_display_pecha = Pecha.from_path(download_pecha("ID4931BF2", Path("tmp")))
root_pecha = Pecha.from_path(download_pecha("I0C6DC77C", Path("tmp")))
prealigned_commentary = Pecha.from_path(download_pecha("IBA00803F", Path("tmp")))

work = PreAlignedCommentarySerializer()
json = work.serialize(root_display_pecha, root_pecha, prealigned_commentary)
write_json("new.json", json)
