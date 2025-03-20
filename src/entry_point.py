
from md_inline import _md_inline_to_md_nodes, _md_node_to_html_leaf_node

def main():
    nodes = _md_inline_to_md_nodes("This is a **bold** statement and _italicized_ text. Here is some `inline code`. Check out [OpenAI](https://openai.com) for more info. Also, look at this cool image: ![AI Logo](https://example.com/logo.png).")
    
    for node in nodes:
        html_node = _md_node_to_html_leaf_node(node)
        print(html_node.to_html())
   
if __name__ == "__main__":
    main()