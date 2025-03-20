import unittest

from html_node import HTMLNode, LeafNode, ParentNode
from md_block import BlockType, _md_block_type, _md_inline_to_md_blocks
from md_inline import _md_node_to_html_leaf_node, _md_inline_to_md_nodes, md_inline_to_html_node
from md_node import MdNode, MdType

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

class Test_MdNode(unittest.TestCase):
    def test_eq(self):
        node = MdNode("This is a text node", MdType.BOLD)
        node2 = MdNode("This is a text node", MdType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = MdNode("This is a text node", MdType.TEXT)
        node2 = MdNode("This is a text node", MdType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_url_none(self):
        node = MdNode("This is a text node", MdType.TEXT, None)
        self.assertIsNotNone(node)

class Test_Md_To_Node(unittest.TestCase):

    # --- Tests for _md_node_to_html_leaf_node ---
    def test_html_node_text(self):
        node = MdNode("plain text", MdType.TEXT)
        html_node = _md_node_to_html_leaf_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "plain text")
    
    def test_html_node_bold(self):
        node = MdNode("bold", MdType.BOLD)
        html_node = _md_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold")
    
    def test_html_node_italic(self):
        node = MdNode("italic", MdType.ITALIC)
        html_node = _md_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic")
    
    def test_html_node_code(self):
        node = MdNode("code", MdType.CODE)
        html_node = _md_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code")
    
    def test_html_node_link(self):
        node = MdNode("link", MdType.LINK, "https://example.com")
        html_node = _md_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "link")
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "https://example.com")
    
    def test_html_node_image(self):
        node = MdNode("image", MdType.IMAGE, "https://example.com")
        html_node = _md_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIn("src", html_node.props)
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["src"], "https://example.com")
        self.assertEqual(html_node.props["alt"], "image")
    
    # --- Tests for md_to_md_nodes ---
    def test_md_nodes_plain(self):
        nodes = _md_inline_to_md_nodes("plain text")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "plain text")
        self.assertEqual(nodes[0].type, MdType.TEXT)
    
    def test_md_nodes_bold(self):
        # Expecting the text to be split into three parts:
        #  "This is ", "**bold**", " text"
        nodes = _md_inline_to_md_nodes("This is **bold** text")
        self.assertGreaterEqual(len(nodes), 3)
        # Check that the middle node is recognized as bold and its content is extracted
        bold_node = nodes[1]
        self.assertEqual(bold_node.type, MdType.BOLD)
        self.assertEqual(bold_node.text, "bold")
    
    def test_md_nodes_italic(self):
        nodes = _md_inline_to_md_nodes("Start _italic_ end")
        self.assertGreaterEqual(len(nodes), 3)
        italic_node = nodes[1]
        self.assertEqual(italic_node.type, MdType.ITALIC)
        self.assertEqual(italic_node.text, "italic")
    
    def test_md_nodes_code(self):
        nodes = _md_inline_to_md_nodes("Before `code` after")
        self.assertGreaterEqual(len(nodes), 3)
        code_node = nodes[1]
        self.assertEqual(code_node.type, MdType.CODE)
        self.assertEqual(code_node.text, "code")
    
    def test_md_nodes_link(self):
        nodes = _md_inline_to_md_nodes("Here is [link](https://example.com) done")
        self.assertGreaterEqual(len(nodes), 3)
        link_node = nodes[1]
        self.assertEqual(link_node.type, MdType.LINK)
        self.assertEqual(link_node.text, "link")
        self.assertEqual(link_node.url, "https://example.com")
    
    def test_md_nodes_image(self):
        nodes = _md_inline_to_md_nodes("Check out ![image](https://example.com) now")
        self.assertGreaterEqual(len(nodes), 3)
        image_node = nodes[1]
        self.assertEqual(image_node.type, MdType.IMAGE)
        self.assertEqual(image_node.text, "image")
        self.assertEqual(image_node.url, "https://example.com")

class Test_Md_To_Blocks(unittest.TestCase):
    def test_md_to_blocks(self):
        text = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

        - This is a list
- with items
        """
        blocks = _md_inline_to_md_blocks(text)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_md_block_type_deduce_paragraph(self):
        paragraph_block = "This is a normal paragraph block.\nWe added this newline to test."
        block_type = _md_block_type(paragraph_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_md_block_type_deduce_code(self):
        code_block = "```printf(\"Hello, world!\")\n// this is a C comment```"
        block_type = _md_block_type(code_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_md_block_type_deduce_quote(self):
        quote_block = "> To be or not to be\n> ...that is the question."
        block_type = _md_block_type(quote_block)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_md_block_type_deduce_ul(self):
        ul_block = "- first item of business\n- Last item to deal with, with extra inline - to test"
        block_type = _md_block_type(ul_block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_md_block_type_deduce_ol(self):
        ul_block = "1. first item of business\n2. Last item to deal with, with extra inline 3. to test"
        block_type = _md_block_type(ul_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

class Test_Md_To_HTML(unittest.TestCase):
    def test_paragraphs(self):
        md = (
            "This is **bolded** paragraph "
            "text in a p "
            "tag here\n\n"
            "This is another paragraph with _italic_ text and `code` here\n\n"
        )

        node = md_inline_to_html_node(md)
        html = node.to_html()
        self.assertMultiLineEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = (
            "```This is text that _should_ remain\n"
            "the **same** even with inline stuff\n```"
        )

        node = md_inline_to_html_node(md)
        html = node.to_html()
        self.assertMultiLineEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        node = md_inline_to_html_node(md)
        html = node.to_html()
        self.assertMultiLineEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_blockquote(self):
        md = "> This is a blockquote\n\n> Another blockquote"
        node = md_inline_to_html_node(md)
        html = node.to_html()
        self.assertMultiLineEqual(
            html,
            "<div><blockquote>This is a blockquote</blockquote><blockquote>Another blockquote</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        node = md_inline_to_html_node(md)
        html = node.to_html()
        self.assertMultiLineEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. First item\n2. Second item\n3. Third item"
        node = md_inline_to_html_node(md)
        html = node.to_html()
        self.assertMultiLineEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_mixed_content(self):
        md = "# Heading\n\nThis is **bold** text with _italic_ and `code`.\n\n- Item A\n- Item B\n\n1. Step 1\n2. Step 2"
        node = md_inline_to_html_node(md)
        html = node.to_html()
        self.assertMultiLineEqual(
            html,
            "<div><h1>Heading</h1><p>This is <b>bold</b> text with <i>italic</i> and <code>code</code>.</p><ul><li>Item A</li><li>Item B</li></ul><ol><li>Step 1</li><li>Step 2</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()