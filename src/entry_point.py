
from static_copy import directory_clear, directory_copy

def main():
    directory_clear("public/")
    directory_copy("static/", "public/")
   
if __name__ == "__main__":
    main()