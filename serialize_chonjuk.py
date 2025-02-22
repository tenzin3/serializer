from pathlib import Path
from utils import read_json, write_json
from typing import Dict, List 


def get_root_text(root_json:Dict) -> List:
    segments = []
    content = root_json["target"]["books"][0]["content"]
    for chapter_content in content:
        for segment in chapter_content:
            segments.append(segment)
    return segments

def get_root_translation_text(root_json):
    segments = []
    content = root_json["source"]["books"][0]["content"]
    for chapter_content in content:
        for segment in chapter_content:
            segments.append(segment)
    return segments


def get_commentary_text(commentary_path):
    segments = []
    commentary_json = read_json(commentary_path)
    content = commentary_json["target"]["books"][0]["content"]
    for chapter_content in content:
        for segment in chapter_content:
            if len(segment) != 0:
                text = segment[0]
            else:
                text = ""
            segments.append(text)

    root_len = 926
    missing_segments = (root_len - len(segments))
    for _ in range(missing_segments):
        segments.append("")
    return segments


def create_final_commentary_json(root_text, commentary_1, commentary_2, commentary_3):
    curr_json = {}
    final_json = []
    for root_segment, commentary_1_segment, commentary_2_segment, commentary_3_segment in zip(root_text, commentary_1, commentary_2, commentary_3):
        curr_json = {
            "root": root_segment,
            "commentary_1": commentary_1_segment,
            "commentary_2": commentary_2_segment,
            "commentary_3": commentary_3_segment
        }
        final_json.append(curr_json)
    write_json(Path("./data_chonjuk/chonjuk.json"), final_json)


def make_root_and_commentary_json():
    root_paths = Path("./data_chonjuk/root/The_Way_of_the_Boddhisattva.json")
    commentary_1_path = Path("./data_chonjuk/commentary/The_commentary_on_the_Bodhicaryavatara_the_drop_of_Nectar_and_the_words_of_Manjusri_and_the_guru.json")
    commentary_2_path = Path("./data_chonjuk/commentary/The_commentary_on_the_intention_of_the_Introduction_to_the_Bodhisattvas_Way_of_Life_called_the_Clarification_of_the_Distinctions.json")
    commentary_3_path = Path("./data_chonjuk/commentary/This_is_the_well_composed_entrance_to_the_bodhisattvas_way_of_life.json")
    root_text = get_root_text(root_paths)
    commentary_1 = get_commentary_text(commentary_1_path)
    commentary_2 = get_commentary_text(commentary_2_path)
    commentary_3 = get_commentary_text(commentary_3_path)
    create_final_commentary_json(root_text, commentary_1, commentary_2, commentary_3)


def create_final_translation_json(root_text, translation_text):
    curr_json = {}
    final_json = []
    for root_segment, translation_segment in zip(root_text, translation_text):
        curr_json = {
            "root": root_segment,
            "sanskrit": translation_segment
        }
        final_json.append(curr_json)
    write_json(Path("./data_chonjuk/translation.json"), final_json)


def make_root_and_translation():
    root_paths = Path("./data_chonjuk/root/The_Way_of_the_Boddhisattva.json")
    translation_path = Path("./data_chonjuk/root/sanskrit.json")
    root_text = get_root_text(root_paths)
    translation_text = get_root_translation_text(translation_path)
    create_final_translation_json(root_text, translation_text)

def get_translation_segment(segment, AI_translation_json):
    for translation in AI_translation_json:
        if translation["root"] == segment:
            return translation["sanskrit"]


def serialize_translation(root_json, AI_translation_json):
    content = []
    chapter = []
    bo_segments = get_root_text(root_json)
    bo_contents = root_json["target"]["books"][0]["content"]
    for num, chapter in enumerate(bo_contents):
        for segment in chapter:
            translation = get_translation_segment(segment, AI_translation_json)
            chapter.append(translation)
        content.append(translation_segements)
    root_json["source"]["books"][0]["content"] = content
    
def serialize_chonjuk_translation():
    AI_translation_json = read_json(Path("./data_chonjuk/root/AI_translation.json"))
    root_json = read_json(Path("./data_chonjuk/input/root/The_Way_of_the_Boddhisattva.json"))
    serialized_json = serialize_translation(root_json, AI_translation_json)

if __name__ == "__main__":
    make_root_and_translation()