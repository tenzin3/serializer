import re 
from pathlib import Path 
from typing import List, Dict
from utils import download_pecha, write_json

from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.translation import TranslationSerializer

from utils import download_pecha

def get_chapter_info(segments:List[str])->List[List[str]]:
    res = {}
    counter = 0
    for idx, segment in enumerate(segments):
        if segment.startswith("ch") or segment.startswith("Ch"):
            counter += 1
        
        if counter not in res:
            res[counter] = [idx+1]
        else:
            res[counter].append(idx+1)

    return res 

def remove_chapter_ann(segments: List[str]) -> List[str]:
    res = []
    for segment in segments:
        segment = re.sub(r"(?i)ch-\d+", "", segment)  # (?i) makes it case-insensitive
        res.append(segment.strip())  # Strip any extra spaces left after removal
    return res

def group_segments_by_chapter(segments: List[str]) -> List[List[str]]:
    """
    Group segments into chapters. A new chapter starts when a segment begins
    with "ch" (case-insensitive). Segments that come before the first chapter marker
    will be grouped together.
    
    Returns a list of chapters, where each chapter is a list of segments.
    """
    chapters = []
    current_chapter = []
    
    for seg in segments:
        # Check if the segment is a chapter marker (e.g., "ch-1", "Ch-2", etc.)
        if re.match(r"(?i)^ch[-\s]?\d+", seg):
            # If there's already content in current_chapter, start a new chapter group.
            if current_chapter:
                chapters.append(current_chapter)
            current_chapter = [seg]
        else:
            current_chapter.append(seg)
            
    if current_chapter:
        chapters.append(current_chapter)
    
    return chapters

def serialize_root():
    root_id = "I7C0673C3"
    root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))
    serialized = TranslationSerializer().serialize(root_pecha)

    tgt_content = serialized["target"]["books"][0]["content"]

    # Extract chapter info
    chapter_info = get_chapter_info(tgt_content)
    # Remove chapter annotation
    segments = remove_chapter_ann(tgt_content)
    # Put into chapters
    chapterized_segments = group_segments_by_chapter(segments)
    
    serialized["target"]["books"][0]["content"] = chapterized_segments



    write_json("chapter.json", chapter_info)
    write_json("jsons/chonjuk/root/chonjuk_root.json", serialized)


if __name__ == "__main__":
    serialize_root()