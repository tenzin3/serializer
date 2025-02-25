from pathlib import Path 
from utils import download_pecha, write_json
from typing import List, Dict 

from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import SimpleCommentarySerializer
from alignment_ann_transfer.commentary import CommentaryAlignmentTransfer


def serialize_commentaries(work_ids: List[Dict], output_path:str):
    for work in work_ids:    
        commentary_id = work["commentary_id"]
        commentary_pecha = Pecha.from_path(download_pecha(commentary_id, Path("tmp")))
        
        root_id = work["root_id"]
        root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))

        root_display_id = work["root_display_id"]
        root_display_pecha = Pecha.from_path(download_pecha(root_display_id, Path("tmp")))
        
        serialized = SimpleCommentarySerializer().serialize(commentary_pecha, root_display_pecha.metadata.title)
        
        # Get Commentary Alignment 
        work = CommentaryAlignmentTransfer()
        tgt_content = work.get_serialized_commentary(root_pecha, root_display_pecha, commentary_pecha)
        
        # Strip the tgt content
        tgt_content = [content.strip() for content in tgt_content]
        serialized["target"]["books"][0]["content"] = [tgt_content]
        write_json(f"{output_path}/{commentary_id}.json", serialized)


if __name__ == "__main__":
    chonjuk_work_ids = [
         {
            "root_display_id": "I7C0673C3",
            "root_id": "I7AF39EB9",
            "commentary_id": "I105531AD"
         }
    ]

    output_path = "jsons/chonjuk/commentary"
    serialize_commentaries(chonjuk_work_ids, output_path=output_path)