from pathlib import Path 

from utils import download_pecha
from stam import AnnotationStore

from alignment_ann_transfer.commentary import CommentaryAlignmentTransfer
from openpecha.pecha import Pecha 
from openpecha.utils import write_json, read_json

# Function to replace keys
def replace_keys(data, key_map):
    return [
        {key_map.get(k, k): v for k, v in entry.items()} 
        for entry in data
    ]


works = [{
            "root_display_id": "I8BCEB363",
            "root_id": "I9943B599",
            "commentary_id": "I22734F80"
         },
         {
            "root_display_id": "I8BCEB363",
            "root_id": "I85E31AAE",
            "commentary_id": "I70BA77E2"
         },
         {
            "root_display_id": "I8BCEB363",
            "root_id": "I02DEEEA9",
            "commentary_id": "I7D9965EE"
         }
]

def get_aligned_segments():
    for work in works:
        root_display_id = work["root_display_id"]
        root_id = work["root_id"]
        commentary_id = work["commentary_id"]

        root_display_pecha = Pecha.from_path(download_pecha(root_display_id, Path("tmp")))
        root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))
        commentary_pecha = Pecha.from_path(download_pecha(commentary_id, Path("tmp")))


        # Define key mapping
        key_map = {
            "root_display_text": "root_display_text",
            "commentary_text": f"{commentary_pecha.id}_commentary_text",
        }

        work = CommentaryAlignmentTransfer()
        serialized_json = work.get_aligned_display_commentary(root_pecha, root_display_pecha, commentary_pecha)
        serialized_json = replace_keys(serialized_json, key_map)
        write_json(f"{commentary_pecha.id}.json", serialized_json)

def combine_aligned_segments():
        
    # Combine all the commentaries
    combined_commentaries = {}
    for work in works:
        commentary_id = work["commentary_id"]
        if combined_commentaries == {}:
            combined_commentaries = read_json(f"{commentary_id}.json")
            continue 
        curr_json = read_json(f"{commentary_id}.json")
        curr_commentary_segments= [entry[f"{commentary_id}_commentary_text"] for entry in curr_json]
        
        # Add the commentary segments to the combined commentaries
        for idx, entry in enumerate(combined_commentaries):
            entry[f"{commentary_id}_commentary_text"] = curr_commentary_segments[idx]

    # Convert commentary texts : List[str] -> str
    for entry in combined_commentaries:
        for work in works:
            commentary_id = work["commentary_id"]
            commentary_text = entry[f"{commentary_id}_commentary_text"]
            combined_text = "\n".join(commentary_text)
            entry[f"{commentary_id}_commentary_text"] = combined_text.strip()

    # Add sanskrit text
    sanskrit_json_path = "sherab_nyingpo_san.json"
    if Path(sanskrit_json_path).exists():
        sanskrit_segments = read_json(sanskrit_json_path)
        for idx, entry in enumerate(combined_commentaries):
            entry["sanskrit_text"] = sanskrit_segments[idx]
    else:
        print("Sanskrit json file not found")

    write_json("combined_commentaries.json", combined_commentaries)

def get_commentary_segments():
    for work in works:
        commentary_id = work["commentary_id"]
        commentary_pecha = Pecha.from_path(download_pecha(commentary_id, Path("tmp")))

        root_id = work["root_id"]
        root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))

        commentary_layer_path = next(commentary_pecha.layer_path.rglob("*.json"))
        commentary_anns = list(AnnotationStore(file=str(commentary_layer_path)))

        root_layer_path = next(root_pecha.layer_path.rglob("*.json"))
        root_anns = list(AnnotationStore(file=str(root_layer_path)))

        segments = []
        for i, commentary_ann in enumerate(commentary_anns):
                root_ann = root_anns[i] if i < len(root_anns) else ""  # Use root_anns[i] if exists, otherwise empty string
                segments.append({
                    "commentary": str(commentary_ann).strip(),
                    "root": str(root_ann).strip()
                })
                    
        write_json(f"{commentary_id}_segments.json", segments)
        

if __name__ == "__main__":
    get_commentary_segments()