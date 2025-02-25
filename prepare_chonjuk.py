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


works = [
         {
            "root_display_id": "I7C0673C3",
            "root_id": "I7AF39EB9",
            "commentary_id": "I105531AD"
         },
         {
            "root_display_id": "I7C0673C3",
            "root_id": "I1B923993",
            "commentary_id": "IB714D443"
         },
         {
            "root_display_id": "I7C0673C3",
            "root_id": "I27D25999",
            "commentary_id": "I9294E222"
         }, 
         {
            "root_display_id": "I7C0673C3",
            "root_id": "I5C855E8C",
            "commentary_id": "IFE85856E"
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
            combined_text = "\n".join(commentary_text) if isinstance(commentary_text, list) else commentary_text
            entry[f"{commentary_id}_commentary_text"] = combined_text.strip() if combined_text else ""

    # Add sanskrit text
    sanskrit_json_path = "chonjuk_san.json"
    if Path(sanskrit_json_path).exists():
        sanskrit_segments = read_json(sanskrit_json_path)
        for idx, entry in enumerate(combined_commentaries):
            entry["sanskrit_text"] = sanskrit_segments[idx]
    else:
        print("chonjuk_san.json Sanskrit json file not found")

    
    # Add the critical edition
    critical_edition_path = "chojuk_with_ce.json"
    if Path(critical_edition_path).exists():
        critical_content = read_json(critical_edition_path)
        critical_segments = [entry["critical_edition"] for entry in critical_content]
        for idx, entry in enumerate(combined_commentaries):
            entry["critical_edition"] = critical_segments[idx]
    else:
        print("chojuk_with_ce.json Critical Edition json file not found")

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
        

def get_sanskrit_segments():
    pecha_id = "I57C874AC"
    pecha = Pecha.from_path(download_pecha(pecha_id, Path("tmp")))


    layer_path = next(pecha.layer_path.rglob("*.json"))
    anns = list(AnnotationStore(file=str(layer_path)))

    segments = [str(ann) for ann in anns]
                
    write_json("chonjuk_san.json", segments)

if __name__ == "__main__":
    # get_sanskrit_segments()
    # get_aligned_segments()
    # combine_aligned_segments()

    get_commentary_segments()