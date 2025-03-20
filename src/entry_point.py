
import os
import re
from md_inline import md_inline_to_html_node
from static_copy import directory_clear, directory_copy

def md_title(md):
    match = re.search(r"^# (.+)", md)
    if match:
        return match.group(1).strip()
    else:
        raise Exception("failed to find md title!")
    
import os

def page_generate(template_path, src_path, dest_path):
    print(f"Generating page from {src_path} to {dest_path} using {template_path}")

    with open(template_path, "r") as template_file:
        template = template_file.read()

    with open(src_path, "r") as md_file:
        md = md_file.read()

    html_node = md_inline_to_html_node(md)
    html = html_node.to_html()
    title = md_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template)


static_dir = "static/"
public_dir = "public/"
page = "index.html"
content_path = "content/index.md"
template_path = "template.html"

def main():
    directory_clear(public_dir)
    directory_copy(static_dir, public_dir)

    page_generate(template_path, content_path, public_dir + page)
   
if __name__ == "__main__":
    main()