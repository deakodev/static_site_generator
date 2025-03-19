import re
from html_node import LeafNode
from markdown_node import MarkdownNode, MarkdownType

markdown_regex_map = [
    { "type": MarkdownType.BOLD, "symbol": "**", "pattern": r"\*\*(?:.*?)\*\*" },
    { "type": MarkdownType.ITALIC, "symbol": "_", "pattern": r"\_(?:.*?)\_" },
    { "type": MarkdownType.CODE, "symbol": "`", "pattern": r"\`(?:.*?)\`" },
    { "type": MarkdownType.LINK, "symbol": "", "pattern": r"(?<!!)\[(.*?)\]\((.*?)\)" },
    { "type": MarkdownType.IMAGE, "symbol": "!", "pattern": r"!\[(.*?)\]\((.*?)\)" }, 
]

def markdown_to_markdown_nodes(text):
    patterns = "|".join(f"({item['pattern']})" for item in markdown_regex_map if item["pattern"] is not None)
    text_split = re.split(patterns, text)
    text_split = [t for t in text_split if t]
    return list(map(_markdown_to_markdown_node, text_split))

def _markdown_to_markdown_node(text):
    match_and_generate = (
         _markdown_node_generate(text, markdown["type"], markdown["symbol"])
        for markdown in markdown_regex_map
        if re.fullmatch(markdown["pattern"], text)
    )
    return next(match_and_generate, MarkdownNode(text, MarkdownType.TEXT))

def _markdown_node_generate(text, type, symbol):
    match type:
        case MarkdownType.BOLD | MarkdownType.ITALIC | MarkdownType.CODE:
            text_stripped = text.strip(symbol)
            return MarkdownNode(text_stripped, type)
        case MarkdownType.LINK | MarkdownType.IMAGE:
            alt, url = text.lstrip(symbol + "[").rstrip(")]").split("](")
            return MarkdownNode(alt, type, url)
        case _:
            return MarkdownNode(text, MarkdownType.TEXT)

def markdown_node_to_html_node(markdown_node):
    match markdown_node.type:
        case MarkdownType.TEXT:
            return LeafNode(None, markdown_node.text, None)
        case MarkdownType.BOLD:
            return LeafNode("b", markdown_node.text, None)
        case MarkdownType.ITALIC:
            return LeafNode("i", markdown_node.text, None)
        case MarkdownType.CODE:
            return LeafNode("code", markdown_node.text, None)
        case MarkdownType.LINK:
            return LeafNode("a", markdown_node.text, {"href": markdown_node.url})
        case MarkdownType.IMAGE:
            return LeafNode("img", "", {"src": markdown_node.url, "alt": markdown_node.text})
        case _: raise ValueError("Invalid MarkdownType: must not be None")