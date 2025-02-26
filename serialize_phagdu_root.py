import re 
from pathlib import Path 
from utils import download_pecha, write_json
from stam import AnnotationStore
from typing import List, Dict 
from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.translation import TranslationSerializer
from utils import read_json



def group_segments_by_chapter(segments: List[str], chapter_info: Dict) -> List[List[str]]:
    """
    Group segments into chapters. A new chapter starts when a segment begins
    with "ch" (case-insensitive). Segments that come before the first chapter marker
    will be grouped together.
    
    Returns a list of chapters, where each chapter is a list of segments.
    """

    chapterized_segments = []
    for chapter_num, segment_indices in chapter_info.items():
        chapter = []
        for idx in segment_indices:
            if idx >= len(segments):
                break
            chapter.append(segments[idx-1])
        chapterized_segments.append(chapter)
    return chapterized_segments

def serialize_bo_root():
    root_id = "IB83348ED"
    root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))

    layer_path = next(root_pecha.layer_path.rglob("*.json"))
    anns = list(AnnotationStore(file=str(layer_path)))

    segments = [str(ann) for ann in anns]

    chapter_info = read_json("jsons/phagdu/chapter.json")
    chapterized_segmenents = group_segments_by_chapter(segments, chapter_info )
    serialized = read_json("jsons/phagdu/root/phagdu_root.json")
    serialized["target"]["books"][0]["content"] = chapterized_segmenents
    write_json("jsons/phagdu/root/phagdu_root.json", serialized)
    write_json("root_segments.json", segments)

if __name__ == "__main__":
    serialize_bo_root()
