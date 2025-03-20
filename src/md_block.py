from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "c"
    QUOTE = "q"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

md_block_map = [
    { "type": BlockType.HEADING, "pattern": r"^#{1,6} .+", "tag": "h", "sub_tag": None },
    { "type": BlockType.QUOTE, "pattern": r"^> .+", "tag": "blockquote", "sub_tag": None },
    { "type": BlockType.CODE, "pattern": r"^```[\s\S]+?```$", "tag": "pre", "sub_tag": "code" },
    { "type": BlockType.UNORDERED_LIST, "pattern": r"^- .+", "tag": "ul", "sub_tag": "li" },
    { "type": BlockType.ORDERED_LIST, "pattern": r"^\d+\. .+", "tag": "ol", "sub_tag": "li" }
]

def _md_block_type(block):
    deduce = (
        b["type"]
        for b in md_block_map
        if re.match(b["pattern"], block)
    )
    return next(deduce, BlockType.PARAGRAPH)

def _md_block_tags(type):
    deduce = (
        (b["tag"], b["sub_tag"])
        for b in md_block_map
        if b["type"] == type
    )
    return next(deduce, ("p", None))

def _md_inline_to_md_blocks(md):
    md_blocks = md.split("\n\n")
    md_blocks_stripped = list(map(str.strip, md_blocks))
    return list(filter(lambda block: block != "", md_blocks_stripped))