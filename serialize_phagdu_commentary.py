import re 
from pathlib import Path 
from utils import download_pecha, write_json, read_json
from typing import List, Dict 

from utils import read_json, write_json, download_pecha
from openpecha.pecha import Pecha 
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import SimpleCommentarySerializer
from alignment_ann_transfer.commentary import CommentaryAlignmentTransfer

def get_chapter_num(segment_num: int) -> int:
   chapter_info: Dict[int, List[str]] =read_json("jsons/phagdu/chapter.json")
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
                
        # Get Commentary Alignment 
        work = CommentaryAlignmentTransfer()
        tgt_content = work.get_serialized_commentary(root_pecha, root_display_pecha, commentary_pecha)
        
        # Strip the tgt content
        tgt_content = [content.strip() for content in tgt_content]
        tgt_content = chapterize_chonjuk_segments(tgt_content)

        # Get the serialized JSON
        root_title = "✨ The Verses Condensing the Perfection of Wisdom"
        serialized = SimpleCommentarySerializer().serialize(commentary_pecha, root_title)
        serialized["target"]["books"][0]["content"] = [tgt_content]
        write_json(f"{output_path}/{commentary_id}.json", serialized)


if __name__ == "__main__":
    sherab_work_ids = [
         {
            "root_display_id": "IB83348ED",
            "root_id": "IBAAAB204",
            "commentary_id": "IDA9229A5"
         },
         {
            "root_display_id": "IB83348ED",
            "root_id": "IEF9637FF",
            "commentary_id": "IB303C1B0"
         },
         {
            "root_display_id": "IB83348ED",
            "root_id": "I2890BFBB",
            "commentary_id": "IF83341B3"
         }
    ]

    output_path = "jsons/phagdu/commentary"
    serialize_commentaries(sherab_work_ids, output_path=output_path)