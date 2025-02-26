import re 
from pathlib import Path 
from utils import download_pecha, write_json
from stam import AnnotationStore

from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.translation import TranslationSerializer
from utils import read_json


def serialize_bo_root():
    root_id = "IB83348ED"
    root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))

    layer_path = next(root_pecha.layer_path.rglob("*.json"))
    anns = list(AnnotationStore(file=str(layer_path)))

    segments = [str(ann) for ann in anns]

    serialized = read_json("jsons/phagdu/root/phagdu_root.json")
    serialized["target"]["books"][0]["content"] = [segments]
    write_json("jsons/phagdu/root/phagdu_root.json", serialized)
    write_json("root_segments.json", segments)

if __name__ == "__main__":
    serialize_bo_root()
