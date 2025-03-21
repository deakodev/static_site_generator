
import sys
from page_gen import pages_generate
from static_copy import directory_clear, directory_copy

static_dir = "static/"
src_dir = "content/"
template_path = "template.html"

def main():
    base_path = sys.argv[1]
    dest_dir = sys.argv[2]
   
    directory_clear(dest_dir)
    directory_copy(static_dir, dest_dir)

    pages_generate(base_path, template_path, src_dir, dest_dir)
   
if __name__ == "__main__":
    main()