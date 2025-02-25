from utils import read_json, write_json
from typing import List, Dict 


def group_segments_by_chapter(segments: List[str], chapter_info: Dict) -> List[List[str]]:
    """
    Group segments into chapters. A new chapter starts when a segment begins
    with "ch" (case-insensitive). Segments that come before the first chapter marker
    will be grouped together.
    
    Returns a list of chapters, where each chapter is a list of segments.
    """

    res = {}
    for chapter_num, segment_indices in chapter_info.items():
        cur_chapter = []
        for idx in segment_indices:
            cur_chapter.append(segments[idx-1])
        res[chapter_num] = cur_chapter
    return res 
    
if __name__ == "__main__":
    critical_edition_content = read_json("chojuk_with_ce.json")
    chapter_info = read_json("chapter.json")
    
    chapterized_critical_content = group_segments_by_chapter(critical_edition_content, chapter_info)
    write_json("chapterized_critical_content.json", chapterized_critical_content)