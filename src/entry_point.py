
from page_gen import pages_generate
from static_copy import directory_clear, directory_copy

static_dir = "static/"
public_dir = "public/"
content_path = "content/"
template_path = "template.html"

def main():
    directory_clear(public_dir)
    directory_copy(static_dir, public_dir)

    pages_generate(template_path, content_path, public_dir)
   
if __name__ == "__main__":
    main()