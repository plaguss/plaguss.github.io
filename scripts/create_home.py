"""Script to generate the content/home/home.md entry. 

To update a given entry, update the corresponding files and run
the script to regenerate the file.
"""

from wasabi import MarkdownRenderer
from pathlib import Path
import textwrap

ROOT = Path(__file__).parent.parent.resolve()

DATA_FOLDER = ROOT / "data"

BLOGS = DATA_FOLDER / "blogs.csv"
PODCASTS = DATA_FOLDER / "podcasts.csv"
BOOKS = DATA_FOLDER / "books.csv"

md = MarkdownRenderer()


def to_raw_html(content: str) -> str:
    """
    This is why:
    https://anaulin.org/blog/hugo-raw-html-shortcode/
    """
    return f"{{{{< rawhtml >}}}}\n {content} \n{{{{< /rawhtml >}}}}"


def do_clickable(element: str, title: str = "Blogs list") -> str:
    """Makes a markdown element clickable."""
    first = to_raw_html(f"<details>\n<summary> {title}:</summary>")
    last = to_raw_html("</details>\n")
    return f"{first}\n\n{element}\n\n{last}"


def read_csv(filename: Path, num_columns: int = 1) -> list[str]:
    if num_columns == 1:  # Blogs
        getter = lambda x: x[0]
    else:  # Podcasts and books
        getter = lambda x: x

    lines = []
    with open(filename, "r") as f:
        for line in f.readlines():
            lines.append(getter(line.replace("\n", "").split(",")))
    return lines


def create_list(data: list[list[str] | str]) -> str:
    # Creates a list of links
    if isinstance(data[0], list):
        return md.list([md.link(items[0], items[1]) for items in data])
    else:
        return md.list([md.link(item, item) for item in data])


def content(blogs: list[str], podcasts: list[list[str]], books: list[list[str]], lang: str = "en") -> str:
    front_matter = textwrap.dedent(
        """---
title: Home
linkTitle: Home
menu: main
weight: 3
---
"""
    )
    md = MarkdownRenderer()
    md.add(front_matter)

    if lang == "en":
        text = """The following lists of items correspond to content that has
helped me to learn (and still does), and would like to keep them
located either for future use or just in case I want to share
with anybody. None of it is in any specific order.
"""
    else:
        text = """Las siguientes listas corresponden a contenido que me ha 
ayudado a aprender (y sigue haciéndolo), y me gustaría mantener lcalizadas
tanto para uso futuro como por si quiero compartirlo con cualquier persona.
No siguen ningún orden específico.
        """

    md.add(text)
    if lang == "en":
        title_blogs = "📔 Blogs I tend to visit from time to time"
        title_books = "📻 Podcasts I listen"
        title_podcasts = "📚 Books I have read (completely or some parts), or that are waiting to be read"
    else:
        title_blogs = "📔 Blogs que suelo visitar de vez en cuando"
        title_books = "📻 Podcasts que escucho"
        title_podcasts = "📚 Books que he leído (completos o alguna parte), o que esperan a ser leídos"

    md.add(
        do_clickable(
            create_list(blogs), title=title_blogs
        )
    )
    md.add(do_clickable(create_list(podcasts), title=title_books))
    md.add(
        do_clickable(
            create_list(books),
            title=title_podcasts,
        )
    )

    return md.text


def create_home_file(filename: Path, lang: str = "en") -> None:
    """Creates the home file."""
    blogs = read_csv(BLOGS)
    podcasts = read_csv(PODCASTS, num_columns=2)
    books = read_csv(BOOKS, num_columns=2)

    data = content(blogs, podcasts, books, lang=lang)

    filename.write_text(data, encoding="utf-8")


if __name__ == "__main__":
    create_home_file(ROOT / "content" / "home" / "_index.en.md")
    create_home_file(ROOT / "content" / "home" / "_index.es.md", lang="es")
