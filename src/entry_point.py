
from markdown_generation import markdown_node_to_html_node, markdown_to_markdown_nodes

def main():
    nodes = markdown_to_markdown_nodes("This is a **bold** statement and _italicized_ text. Here is some `inline code`. Check out [OpenAI](https://openai.com) for more info. Also, look at this cool image: ![AI Logo](https://example.com/logo.png).")
    
    for node in nodes:
        html_node = markdown_node_to_html_node(node)
        print(html_node.to_html())
   
if __name__ == "__main__":
    main()