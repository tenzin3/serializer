import re 
from pathlib import Path 
from utils import download_pecha, write_json, read_json
from typing import List, Dict 

from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import SimpleCommentarySerializer
from alignment_ann_transfer.commentary import CommentaryAlignmentTransfer

def get_chapter_num(segment_num: int) -> int:
   chapter_info: Dict[int, List[str]] =read_json("jsons/chonjuk/chapter.json")
   for chapter_num, segment_indices in chapter_info.items():
         if segment_num in segment_indices:
            return int(chapter_num)
         


def chapterize_chonjuk_segments(segments: List[str]) -> List[List[str]]:
   """
   Group segments into chapters. A new chapter starts when a segment begins
   chapter info has chapter number as key and list of segment indices as value
   """
   chapter_info: Dict[int, List[str]] =read_json("jsons/chonjuk/chapter.json")
   res = []
   curr_chapter = []
   last_chapter = 1
   for segment in segments:
      pattern = re.compile(r'<(\d+)><(\d+)>')
      match = pattern.search(segment)
      if match:
         segment_num = int(match.group(2))
         
         chapter_num = get_chapter_num(segment_num)
         if chapter_num != last_chapter:
               res.append(curr_chapter)
               curr_chapter = []
               last_chapter = chapter_num
         else:
            curr_chapter.append(segment)
      else:
         curr_chapter.append(segment)
   if curr_chapter:
      res.append(curr_chapter)
   return res
            
            

def serialize_commentaries(work_ids: List[Dict], output_path:str):
    for work in work_ids:    
        commentary_id = work["commentary_id"]
        commentary_pecha = Pecha.from_path(download_pecha(commentary_id, Path("tmp")))
        
        root_id = work["root_id"]
        root_pecha = Pecha.from_path(download_pecha(root_id, Path("tmp")))

        root_display_id = work["root_display_id"]
        root_display_pecha = Pecha.from_path(download_pecha(root_display_id, Path("tmp")))
        
        # Get serialized JSON with metadata
        serialized = read_json(f"jsons/chonjuk/commentary/{commentary_id}.json")

        # Get Commentary Alignment 
        work = CommentaryAlignmentTransfer()
        tgt_content = work.get_serialized_commentary(root_pecha, root_display_pecha, commentary_pecha)

        # Strip the tgt content
        tgt_content = [content.strip() for content in tgt_content]
        tgt_content = chapterize_chonjuk_segments(tgt_content)
        serialized["target"]["books"][0]["content"] = tgt_content
        write_json(f"{output_path}/{commentary_id}.json", serialized)


if __name__ == "__main__":
    chonjuk_work_ids = [
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
         }
    ]

    output_path = "jsons/chonjuk/commentary"
    serialize_commentaries(chonjuk_work_ids, output_path=output_path)