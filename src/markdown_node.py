from enum import Enum

class MarkdownType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class MarkdownNode:
    def __init__(self, text, type, url = None):
        self.text = text
        self.type = type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.type == other.type and self.url == other.url

    def __repr__(self):
        return f"MarkdownNode({self.text}, {self.type.value}, {self.url})"