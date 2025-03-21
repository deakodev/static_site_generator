import re
from html_node import LeafNode, ParentNode
from md_block import BlockType, _md_block_tags, _md_block_type, _md_inline_to_md_blocks
from md_node import MdNode, MdType

md_regex_map = [
    { "type": MdType.BOLD, "symbol": "**", "pattern": r"\*\*(?:.*?)\*\*" },
    { "type": MdType.ITALIC, "symbol": "_", "pattern": r"\_(?:.*?)\_" },
    { "type": MdType.CODE, "symbol": "`", "pattern": r"\`(?:.*?)\`" },
    { "type": MdType.LINK, "symbol": "", "pattern": r"(?<!!)\[(?:.*?)\]\((?:.*?)\)" },
    { "type": MdType.IMAGE, "symbol": "!", "pattern": r"!\[(?:.*?)\]\((?:.*?)\)" } 
]

def md_inline_to_html_node(md):
    html_nodes = []
    md_blocks = _md_inline_to_md_blocks(md)
    for block in md_blocks:
        parent_node = _md_block_to_html_parent_node(block)
        html_nodes.append(parent_node)
    return ParentNode("div", html_nodes)

def _md_inline_to_md_nodes(md):
    patterns = "|".join(f"({item['pattern']})" for item in md_regex_map)
    md_split = re.split(patterns, md)
    md_split = [t for t in md_split if t]
    return list(map(_to_md_node, md_split))

def _to_md_node(md):
    match_and_generate = (
         _md_node_generate(md, md_regex["type"], md_regex["symbol"])
        for md_regex in md_regex_map
        if re.fullmatch(md_regex["pattern"], md)
    )
    return next(match_and_generate, MdNode(md, MdType.TEXT))

def _md_node_generate(md, type, symbol):
    match type:
        case MdType.BOLD | MdType.ITALIC | MdType.CODE:
            md_stripped = md.strip(symbol)
            return MdNode(md_stripped, type)
        case MdType.LINK | MdType.IMAGE:
            md_alt, md_url = md.lstrip(symbol + "[").rstrip(")]").split("](")
            return MdNode(md_alt, type, md_url)
        case _:
            return MdNode(md, MdType.TEXT)
        
def _md_block_to_html_parent_node(block):
    type = _md_block_type(block)
    tag, sub_tag = _md_block_tags(type)
    if type != BlockType.CODE:
        match type:
            case BlockType.QUOTE:
                pattern = r"^> (.+)"
                items = re.findall(pattern, block, flags=re.MULTILINE)
                block = "".join(f"\n{item}" for item in items)
            case BlockType.HEADING:
                match = re.match(r"^(#+)", block)
                tag = tag + str(len(match.group(1))) 
                block = block.strip("#").strip()
            case BlockType.UNORDERED_LIST:
                pattern = r"^- (.+)"
                items = re.findall(pattern, block, flags=re.MULTILINE)
                block = "".join(f"<li>{item}</li>" for item in items)
            case BlockType.ORDERED_LIST:
                pattern = r"^\d+\.\s(.+)"
                items = re.findall(pattern, block, flags=re.MULTILINE)
                block = "".join(f"<li>{item}</li>" for item in items)
        children = _md_inline_to_md_nodes(block)
        children = list(map(_md_node_to_html_leaf_node, children))
    else:
        block = block.strip("`")
        children = [LeafNode(sub_tag, block, None)]
    return ParentNode(tag, children)

def _md_node_to_html_leaf_node(md_node):
    match md_node.type:
        case MdType.TEXT:
            return LeafNode(None, md_node.text, None)
        case MdType.BOLD:
            return LeafNode("b", md_node.text, None)
        case MdType.ITALIC:
            return LeafNode("i", md_node.text, None)
        case MdType.CODE:
            return LeafNode("code", md_node.text, None)
        case MdType.LINK:
            return LeafNode("a", md_node.text, {"href": md_node.url})
        case MdType.IMAGE:
            return LeafNode("img", "", {"src": md_node.url, "alt": md_node.text})
        case _: raise ValueError("Invalid MdType: must not be None")