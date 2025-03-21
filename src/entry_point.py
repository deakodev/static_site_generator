
import sys
from page_gen import pages_generate
from static_copy import directory_clear, directory_copy

static_dir = "static/"
public_dir = "docs/"
content_path = "content/"
template_path = "template.html"

def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
   
    directory_clear(public_dir)
    directory_copy(static_dir, public_dir)

    pages_generate(base_path, template_path, content_path, public_dir)
   
if __name__ == "__main__":
    main()