import re 
import io
import json 
import re 
import requests
import zipfile
import shutil

from pathlib import Path 

from typing import List, Dict

from utils import read_json, write_json, download_pecha, normalize_escape_chars, remove_symbols


from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.translation import TranslationSerializer


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
            chapter.append(segments[idx-1])
        chapterized_segments.append(chapter)
    return chapterized_segments
    

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
    chapterized_segments = group_segments_by_chapter(segments, chapter_info)
    
    serialized["target"]["books"][0]["content"] = chapterized_segments

    write_json("chapter.json", chapter_info)
    write_json("jsons/chonjuk/root/chonjuk_root.json", serialized)


if __name__ == "__main__":
    # serialize_root()
    # san_segments = read_json("jsons/chonjuk/root/chonjuk_san_segments.json")
    chapter_info = read_json("jsons/chonjuk/chapter.json")

    # san_chapterized_segments = group_segments_by_chapter(san_segments, chapter_info)
    # write_json("jsons/chonjuk/root/chonjuk_san_chapterized.json", san_chapterized_segments)

    translation_content = read_json("downloads/data_chonjuk/chunjuk_en_translations.json")
    keys = ["plaintext_translation", "combined_commentary"]

    res = {k:[] for k in keys}
    for content in translation_content:
        for key in keys:
            text = content[key]
            text = normalize_escape_chars(text)
            text = remove_symbols(text)
            res[key].append(text)
    
    for k, segments in res.items():
        chapterized_segments = group_segments_by_chapter(segments, chapter_info)
        write_json(f"{k}.json", chapterized_segments)