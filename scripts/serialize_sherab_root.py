import re 
from pathlib import Path 
from utils import download_pecha, write_json

from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.translation import TranslationSerializer
from utils import read_json


def serialize_bo_root():
    root_id = "I8BCEB363"
    root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))
    serialized = TranslationSerializer().serialize(root_pecha)
    write_json("jsons/sherab/root/sherab_root.json", serialized)



ENGLISH_TITLE = "The Heart of the Perfection of Wisdom"
EN_TITLE_MAP = {
        "translation" : f"{ENGLISH_TITLE} AI Draft, Feb 2025",
        "word by word translation": f"{ENGLISH_TITLE} Word by Word, Feb 2025",  
        "plaintext_translation": f"{ENGLISH_TITLE} Easy to Read, Feb 2025",
        "combined_commentary": f"{ENGLISH_TITLE} Combined Commentary, Feb 2025"
}

CHINESE_TITLE = "般若波羅密多心經"
ZH_TITLE_MAP = {
        "translation" : f"{CHINESE_TITLE} AI Draft, Feb 2025",
        "word by word translation": f"{CHINESE_TITLE} Word by Word, Feb 2025",  
        "plaintext_translation": f"{CHINESE_TITLE} Easy to Read, Feb 2025",
        "combined_commentary": f"{CHINESE_TITLE} Combined Commentary, Feb 2025"
}


def remove_symbols(text: str) -> str:
    """
    Remove hashtag
    """
    text = text.replace("#", "")
    return text

def normalize_escape_chars(text: str) -> str:
    text = text.replace('\"', "'").replace("\\/", "/")
    return text

def serialize_en_translations():
    bo_json = read_json("jsons/sherab/root/sherab_root.json")
    
    translations = read_json("downloads/sherab/sherp_nyingpo_final.json")

    keys = translations[0].keys()
    res = {}

    for key in keys:
        if key == "source":
            continue
        res[key] = []

    for translation in translations:
        for key in keys:
            if key == "source":
                continue

            # normalize escape characters
            text = translation[key]
            text = normalize_escape_chars(text)
            text = remove_symbols(text)
            text = text.strip()
            res[key].append(text)
    
    new_src_books = []
    for translation_name, content in res.items():
        title_on_pecha  = EN_TITLE_MAP[translation_name]
        book_metadata = {
            "title": title_on_pecha,
            "language": "en",
            "versionSource": "Cluade AI",
            "direction": "ltr",
            "completestatus": "done",
            "content": [content]
        }
        new_src_books.append(book_metadata)
    
    bo_json["source"]["books"].extend(new_src_books) 
    write_json("jsons/sherab/root/sherab_en_translations.json", bo_json)


def serialize_zh_translations():
    bo_json = read_json("jsons/sherab/root/sherab_root.json")
    
    translations = read_json("downloads/sherab/sherp_nyingpo_chinese_final.json")

    keys = translations[0].keys()
    res = {}

    for key in keys:
        if key == "source":
            continue
        res[key] = []

    for translation in translations:
        for key in keys:
            if key == "source":
                continue

            # normalize escape characters
            text = translation[key]
            text = normalize_escape_chars(text)
            text = remove_symbols(text)
            text = text.strip()
            res[key].append(text)
    
    new_src_books = []
    for translation_name, content in res.items():
        title_on_pecha  = ZH_TITLE_MAP[translation_name]
        book_metadata = {
            "title": title_on_pecha,
            "language": "en",
            "versionSource": "Cluade AI",
            "direction": "ltr",
            "completestatus": "done",
            "content": [content]
        }
        new_src_books.append(book_metadata)
    
    bo_json["source"]["books"].extend(new_src_books) 
    write_json("jsons/sherab/root/sherab_zh_translations.json", bo_json)


if __name__ == "__main__":
    serialize_zh_translations()
