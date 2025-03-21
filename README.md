# Static Site Generator

This is my ground-up implementation of a static site generator, built ansd inspired by Boot.dev. The generator converts Markdown files into a fully functional static website using Python. I built this project to learn more about file handling, templating, and creating a simple command-line tool within Python.

## Features

- **Markdown Conversion:** Transforms Markdown content into HTML.
- **Templating System:** Uses an HTML template to ensure a consistent layout.
- **Asset Management:** Automatically copies static assets (e.g., CSS, images) to the output folder.
- **CLI Tool:** Easily specify input and output directories via shell scripts.
- **Minimal Dependencies:** Lightweight and straightforward for learning purposes.

## Usage

- **Generating a Site:**

  Add your markdown files in the /content dir then run...

  Locally:

  ```bash
  ./scripts/debug.sh
  ```

  Production:

  ```bash
  ./scripts/build.sh
  ```

  To run included unit tests:

  ```bash
  ./scripts/test.sh
  ```

## Project Structure

```plaintext
.
├── content/         # Markdown content files
├── public/          # Generated static site output
├── static/          # Static assets (CSS, images, etc.)
├── src/             # Source code for the generator
├── scripts/         # Build locally or production, tests
├── template.html    # HTML template used for pages
```

## Personal Reflection

Working on this project has been an incredibly rewarding experience. I delved into Markdown parsing, file I/O, and templating with Python, and I now have a clearer understanding of how static site generators work. It’s been a great stepping stone for exploring more advanced web development techniques.

## Future Improvements

- **Watch Mode:** Implement a file watcher to automatically regenerate the site on content changes.
- **Theme Support:** Allow custom themes and layouts for greater flexibility.
- **Enhanced Markdown:** Add features like syntax highlighting for code blocks and improved Markdown extensions.
- **Performance Optimizations:** Further optimize file processing for larger websites.

## License

This project is open source under the [MIT License](LICENSE).

## Acknowledgments

A big thank you to Boot.dev for the guidance and inspiration throughout this project.
