
import sys
from page_gen import pages_generate
from static_copy import directory_clear, directory_copy

static_dir = "static/"
dest_dir = "docs/"
src_dir = "content/"
template_path = "template.html"

def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
   
    directory_clear(dest_dir)
    directory_copy(static_dir, dest_dir)

    pages_generate(base_path, template_path, src_dir, dest_dir)
   
if __name__ == "__main__":
    main()