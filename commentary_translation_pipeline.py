from typing import Dict, List 

from utils import read_json, write_json
from root_translation_pipeline import prepare_content, get_segments



def get_chapter_and_segment_mapping(text:Dict):
    """
    Get Chapter information with segment number.
    1.Read 'target' content
    2.Loop throught chapters
    3.Get chapter number and segment number
    """
    tgt_content = text["target"]["books"][0]["content"]
    
    map = {}
    segment_no = 1
    for chapter_no, chapter_content in enumerate(tgt_content, start=1):
        chapter_map = []
        for segment_content in chapter_content:
            if not segment_content:
                raise ValueError(f"Segment content is empty for chapter {chapter_no} {segment_no}")
            chapter_map.append(segment_no)
            segment_no += 1
        map[chapter_no] = chapter_map
    return map 

def commentary_translation_pipeline(ai_json:Dict, commentary_json:Dict, translation_name:str, metadata:Dict)->Dict:
    # Get Root translation only
    commentary_translation: List[str] = get_segments(ai_json, translation_name)

    # Get chapter and segment number mapping
    chapter_segment_map: Dict[int, List] = get_chapter_and_segment_mapping(commentary_json)

    # Get content by replacing segment number with segment
    content = prepare_content(chapter_segment_map, commentary_translation)

    # Replace Root JSON content and metadata
    commentary_json["source"]["books"][0] = {**metadata, "content": content}

    return commentary_json

if __name__ == "__main__":
    ai_json = read_json("downloads/data_chonjuk/cleaned_data_3 (1).json")

    commentary_json = read_json("downloads/data_chonjuk/input/commentary/The_commentary_on_the_Bodhicaryavatara_the_drop_of_Nectar_and_the_words_of_Manjusri_and_the_guru.json")
    
    new_metadata = {
                "title": "The Way of the Bodhisattva Commentary",
                "language": "en",
                "versionSource": "",
                "completestatus": "in_progress",
                "direction": "ltr"
    }
    
    translation_name = "commentary1_translation"
    new_root_json = commentary_translation_pipeline(ai_json, commentary_json, translation_name, new_metadata)

    write_json("new.json", new_root_json)