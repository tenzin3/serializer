from utils import read_json, write_json
from typing import Dict, List 

def get_segments(list_of_segments: Dict, key:str)->List[str]:
    """
    INPUT: 
     list_of_segments = [
                    {
                        "source": "རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།\n",
                        "commentary1_translation": "The Written Commentary ,..",
                        "commentary2_translation": "Bodhicaryāvatāra-tātparya-pañjikā-viśeṣa-dyotanī-nāma",
                        "commentary3_translation": "Commentary on the Guide to the Bodhisattva's Way of Life",
                        "plaintext_translation": "Bodhisattvacaryāvatāra",
                        "combined_commentary": "This opening line represents ."
                    }, ...
                ]
    key: "source:

    OUTPUT:
    segments = ["རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།\n", ...]
    
    """
    segments = []
    for content in list_of_segments:
        if key not in content:
            raise ValueError(f"Key {key} not found in the content")
        
        segments.append(content[key])
    return segments

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

def prepare_content(chapter_map: Dict[int, List], segments: List[str]):
    """
    INPUT: chapter_map: Chapter and segment number mapping
    PROCESS:Prepare content with chapter number and actual segment.
    
    1. Loop through chapter_map
    2. Replace segment number with segment
    """
    content = []
    for chapter_no, segment_nos in chapter_map.items():
        chapter_content = []
        for segment_no in segment_nos:
            segment = segments[segment_no-1]
            segment = segment if segment else ""
            chapter_content.append(segment)
        content.append(chapter_content)
    return content

def root_translation_pipeline(ai_json:Dict, root_json:Dict, metadata:Dict)->Dict:
    # Get Root translation only
    root_translation: List[str] = get_segments(ai_json, "plaintext_translation")

    # Get chapter and segment number mapping
    chapter_segment_map: Dict[int, List] = get_chapter_and_segment_mapping(root_json)

    # Get content by replacing segment number with segment
    content = prepare_content(chapter_segment_map, root_translation)

    # Replace Root JSON content and metadata
    root_json["source"]["books"][0] = {**new_metadata, "content": content}

    return root_json

if __name__ == "__main__":
    ai_json = read_json("downloads/data_chonjuk/cleaned_data_3 (1).json")

    root_json = read_json("downloads/data_chonjuk/input/root/The_Way_of_the_Boddhisattva.json")
    
    new_metadata = {
                "title": "The Way of the Bodhisattva",
                "language": "en",
                "versionSource": "",
                "completestatus": "in_progress",
                "direction": "ltr"
    }
    
    new_root_json = root_translation_pipeline(ai_json, root_json, new_metadata)

    write_json("new.json", new_root_json)