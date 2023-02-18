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
PODCASTS = DATA_FOLDER / "blogs.csv"

blog = Path(".") / "data/blogs.csv"

md = MarkdownRenderer()


def to_raw_html(content: str) -> str:
    """
    This is why:
    https://anaulin.org/blog/hugo-raw-html-shortcode/
    """
    return f"{{{{< rawhtml >}}}}\n {content} \n{{{{< /rawhtml >}}}}"


def do_clickable(element: str, title: str = "Blogs list") -> str:
    """Makes a markdown element clickable. """
    first = to_raw_html(f"<details>\n<summary> {title}:</summary>")
    last = to_raw_html("</details>\n")
    return f"{first}\n\n{element}\n\n{last}"


def read_file(filename: Path) -> list[str]:
    lines = []
    with open(filename, "r") as f:
        f.readline()  # The first line are the headers, ignore
        for line in f.readlines():
            lines.append(line.replace("\n", "").split(",")[0])
    return lines


def create_list(data: list[str]) -> str:
    # Creates a list of links
    return md.list([md.link(blog, blog) for blog in data])


def content(blogs: list[list[str]]) -> str:
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

    md.add(
"""The following table contains a series of blogs that I've come
across at any point in time and found anything interesting. Its just a
personal table to keep track of interesting info, with no specific order.
"""
    )

    # md.add(create_list(blogs))
    md.add(do_clickable(create_list(blogs)))

    return md.text


def create_home_file(filename: Path) -> None:
    """Creates the home file. """
    blogs = read_file(BLOGS)

    data = content(blogs)

    filename.write_text(data, encoding="utf-8")


if __name__ == "__main__":
    create_home_file(ROOT / "content" / "home" / "home.md")
