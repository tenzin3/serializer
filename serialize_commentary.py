from pathlib import Path 
from utils import download_pecha, write_json

from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import SimpleCommentarySerializer
from alignment_ann_transfer.commentary import CommentaryAlignmentTransfer

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

def serialize_commentaries():
    for work in works:    
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
        write_json(f"jsons/sherab/commentary/{commentary_id}.json", serialized)


if __name__ == "__main__":
    serialize_commentaries()