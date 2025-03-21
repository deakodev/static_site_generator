
import os
from pathlib import Path
import re
import shutil
from md_inline import md_inline_to_html_node

def md_title(md):
    match = re.search(r"^# (.+)", md)
    if match:
        return match.group(1).strip()
    else:
        raise Exception("failed to find md title!")

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
        
def pages_generate(template_path, src_dir, dest_dir):
    src_items = os.listdir(src_dir)
    for item in src_items:
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(src_path):
            dest_path = dest_path.replace(".md", ".html")
            page_generate(template_path, src_path, dest_path)
        else:
            pages_generate(template_path, src_path, dest_path)