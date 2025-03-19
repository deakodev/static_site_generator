import unittest

from html_node import HTMLNode, LeafNode, ParentNode
from markdown_generation import markdown_node_to_html_node, markdown_to_markdown_nodes
from markdown_node import MarkdownNode, MarkdownType

class Test_HTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode("p", "value")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_props_to_html(self):
        node_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "link", None, node_props)
        node_html = node.props_to_html()
        self.assertEqual(node_html, " href=\"https://www.google.com\" target=\"_blank\"")
    
    def test_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"key": "value"})
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'key': 'value'})",
        )

class Test_LeafNode(unittest.TestCase):
    def test_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_a(self):
        node = LeafNode("a", "Click this link!", { "href": "https://www.google.com" })
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click this link!</a>")

    def test_to_html_image_mult_props(self):
        node = LeafNode("div", "This is a div!", { "class": "border-500-green", "src": "https://www.google.com" })
        self.assertEqual(node.to_html(), "<div class=\"border-500-green\" src=\"https://www.google.com\">This is a div!</div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

class Test_ParentNode(unittest.TestCase):
    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertIsNotNone(parent_node.to_html()) 

    def test_to_html_without_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", None)
            parent_node.to_html()

class Test_MarkdownNode(unittest.TestCase):
    def test_eq(self):
        node = MarkdownNode("This is a text node", MarkdownType.BOLD)
        node2 = MarkdownNode("This is a text node", MarkdownType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = MarkdownNode("This is a text node", MarkdownType.TEXT)
        node2 = MarkdownNode("This is a text node", MarkdownType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_url_none(self):
        node = MarkdownNode("This is a text node", MarkdownType.TEXT, None)
        self.assertIsNotNone(node)

class Test_Markdown_Conversion(unittest.TestCase):

    # --- Tests for markdown_node_to_html_node ---
    def test_html_node_text(self):
        node = MarkdownNode("plain text", MarkdownType.TEXT)
        html_node = markdown_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "plain text")
    
    def test_html_node_bold(self):
        node = MarkdownNode("bold", MarkdownType.BOLD)
        html_node = markdown_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold")
    
    def test_html_node_italic(self):
        node = MarkdownNode("italic", MarkdownType.ITALIC)
        html_node = markdown_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic")
    
    def test_html_node_code(self):
        node = MarkdownNode("code", MarkdownType.CODE)
        html_node = markdown_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code")
    
    def test_html_node_link(self):
        node = MarkdownNode("link", MarkdownType.LINK, "https://example.com")
        html_node = markdown_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "link")
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "https://example.com")
    
    def test_html_node_image(self):
        node = MarkdownNode("image", MarkdownType.IMAGE, "https://example.com")
        html_node = markdown_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIn("src", html_node.props)
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["src"], "https://example.com")
        self.assertEqual(html_node.props["alt"], "image")
    
    # --- Tests for markdown_to_markdown_nodes ---
    def test_markdown_nodes_plain(self):
        nodes = markdown_to_markdown_nodes("plain text")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "plain text")
        self.assertEqual(nodes[0].type, MarkdownType.TEXT)
    
    def test_markdown_nodes_bold(self):
        # Expecting the text to be split into three parts:
        #  "This is ", "**bold**", " text"
        nodes = markdown_to_markdown_nodes("This is **bold** text")
        self.assertGreaterEqual(len(nodes), 3)
        # Check that the middle node is recognized as bold and its content is extracted
        bold_node = nodes[1]
        self.assertEqual(bold_node.type, MarkdownType.BOLD)
        self.assertEqual(bold_node.text, "bold")
    
    def test_markdown_nodes_italic(self):
        nodes = markdown_to_markdown_nodes("Start _italic_ end")
        self.assertGreaterEqual(len(nodes), 3)
        italic_node = nodes[1]
        self.assertEqual(italic_node.type, MarkdownType.ITALIC)
        self.assertEqual(italic_node.text, "italic")
    
    def test_markdown_nodes_code(self):
        nodes = markdown_to_markdown_nodes("Before `code` after")
        self.assertGreaterEqual(len(nodes), 3)
        code_node = nodes[1]
        self.assertEqual(code_node.type, MarkdownType.CODE)
        self.assertEqual(code_node.text, "code")
    
    def test_markdown_nodes_link(self):
        nodes = markdown_to_markdown_nodes("Here is [link](https://example.com) done")
        self.assertGreaterEqual(len(nodes), 3)
        link_node = nodes[1]
        self.assertEqual(link_node.type, MarkdownType.LINK)
        self.assertEqual(link_node.text, "link")
        self.assertEqual(link_node.url, "https://example.com")
    
    def test_markdown_nodes_image(self):
        nodes = markdown_to_markdown_nodes("Check out ![image](https://example.com) now")
        self.assertGreaterEqual(len(nodes), 3)
        image_node = nodes[1]
        self.assertEqual(image_node.type, MarkdownType.IMAGE)
        self.assertEqual(image_node.text, "image")
        self.assertEqual(image_node.url, "https://example.com")

if __name__ == "__main__":
    unittest.main()