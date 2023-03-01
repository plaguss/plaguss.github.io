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


def add_projects(lang: str = "en") -> str:
    md_proj = MarkdownRenderer()
    if lang == "en":
        md_proj.add(md.title(2, "Projects"))

        translate_md = md.code("translate_md")
        translate_md += """: {}. A client to translate markdwon files from english to spanish,
makes use of {} for the translation service.""".format(
            md.bold("Work in progress"),
            md.link("spanglish", "https://github.com/plaguss/spanglish"),
        )

        helpner_core = md.link(
            md.code("helpner-core"), "https://github.com/plaguss/helpner-core"
        )
        cli_help_maker = md.link(
            md.code("cli-help-maker"), "https://github.com/plaguss/cli-help-maker"
        )
        helpner = md.link(md.code("helpner"), "https://github.com/plaguss/helpner")
        helpner += """: A python console program to extract entities from command line 
programs' help messages. It makes use of two intermediate libraries: {} as a
spaCy template, and {} as a data generator.""".format(
            helpner_core, cli_help_maker
        )

        movinets_for_crossfit = md.code("MoViNets for CrossFit")
        movinets_for_crossfit += """: A plotly dash app to classify CrossFit movements {} 
deployed to AWS, based on a finetuned version of {}, the tensorflow implementation of 
a network to classify human movements in videoclips. The repos still need to be better
organized, but los entre los comopnentes, a helper library can be seen here: {}, the 
code for the front here: {}, and here the pieces related to the cloud: {}.
""".format(
            md.italic("(no longer)"),
            md.link(
                "Mobile Video Networks (MoViNets)",
                "https://github.com/tensorflow/models/tree/master/official/projects/movinet",
            ),
            md.link("movinets_helper", "https://github.com/plaguss/movinets_helper"),
            md.link(
                "movinets_dash_app", "https://github.com/plaguss/movinets_dash_app"
            ),
            md.link(
                "lambda_aws", "https://github.com/plaguss/tfm-misc/tree/main/lambda_aws"
            ),
        )

        pytokei = md.link(md.code("pytokei"), "https://github.com/plaguss/pytokei")
        pytokei += f""": Python bindings to {md.link("tokei", "https://github.com/XAMPPRocky/tokei")}, 
a rust program to extract statistics from your code."""

        biblioteca_cidaen = md.link(
            md.code("biblioteca-cidaen"), "https://github.com/plaguss/biblioteca-cidaen"
        )
        biblioteca_cidaen += """: {}. A prototype for an 'online library' where the students could
share their master's thesis.
Even though its tailored for the master's program that I coursed, 
it can be used as an interesting approach to introduce students
to collaboration in GitHub and the Pull Request mecanism.""".format(
            md.italic("(written in spanish)")
        )
        md_proj.add(
            md.list(
                [
                    translate_md,
                    helpner,
                    movinets_for_crossfit,
                    pytokei,
                    biblioteca_cidaen,
                ]
            )
        )

    else:
        md_proj.add(md.title(2, "Proyectos"))

        translate_md = md.code("translate_md")
        translate_md += """: {}. Un cliente para traducir ficheros markdown de inglés a 
castellano, hace uso de {} para el servicio de traducción.""".format(
            md.bold("Work in progress"),
            md.link("spanglish", "https://github.com/plaguss/spanglish"),
        )

        helpner_core = md.link(
            md.code("helpner-core"), "https://github.com/plaguss/helpner-core"
        )
        cli_help_maker = md.link(
            md.code("cli-help-maker"), "https://github.com/plaguss/cli-help-maker"
        )
        helpner = md.link(md.code("helpner"), "https://github.com/plaguss/helpner")
        helpner += """: Un programa por consola escrito en python para extraer entidades
de mensajes de ayuda de programas por consola. Hace uso de dos librerías intermedias: {}
una plantilla de spaCy, y {} como generador de datos""".format(
            helpner_core, cli_help_maker
        )

        movinets_for_crossfit = md.code("MoViNets para CrossFit")
        movinets_for_crossfit += """: Una aplicación escrita en {} para clasificar movimientos
de CrossFit {} desplegada en AWS, basada en una versión 'fine tuned' de {}, la implementación
en tensorflow de una red para clasificar movimientos humanos en videoclips. Los repositorios
aún necesitan ponerse al día, pero entre los componentes, una librería de ayuda se puede ver
aquí: {}, el código para el front aquí: {}, y las piezas relacionadas con la nube aquí: {}""".format(
            md.link("plotly dash", "https://dash.plotly.com/"),
            md.italic("(no actualmente)"),
            md.link(
                "Mobile Video Networks (MoViNets)",
                "https://github.com/tensorflow/models/tree/master/official/projects/movinet",
            ),
            md.link("movinets_helper", "https://github.com/plaguss/movinets_helper"),
            md.link(
                "movinets_dash_app", "https://github.com/plaguss/movinets_dash_app"
            ),
            md.link(
                "lambda_aws", "https://github.com/plaguss/tfm-misc/tree/main/lambda_aws"
            ),
        )

        pytokei = md.link(md.code("pytokei"), "https://github.com/plaguss/pytokei")
        pytokei += f""": Bindings en python para {md.link("tokei", "https://github.com/XAMPPRocky/tokei")}, 
un programa escrito en rust para extraer estadísticos sobre el código fuente."""

        biblioteca_cidaen = md.link(
            md.code("biblioteca-cidaen"), "https://github.com/plaguss/biblioteca-cidaen"
        )
        biblioteca_cidaen += """: {}. Prototipo de una 'librería online' donde los estudiantes
podrían compartir sus trabajos (de máster en este caso).
Aunque está hecho a la medida del programa de máster que cursé, se puede
utilizar como un enfoque interesante para ayudar introducir a los alumnos
a la colaboración en GitHub mediante Pull Requests.""".format(
            md.italic("(written in spanish)")
        )
        md_proj.add(
            md.list(
                [
                    translate_md,
                    helpner,
                    movinets_for_crossfit,
                    pytokei,
                    biblioteca_cidaen,
                ]
            )
        )


    return md_proj.text


def content(
    blogs: list[str],
    podcasts: list[list[str]],
    books: list[list[str]],
    lang: str = "en",
) -> str:
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

    projects = add_projects(lang=lang)
    md.add(projects)

    if lang == "en":
        text = md.title(2, "Some wonderful resources")
        text += """\nThe following lists of items correspond to content that has
helped me to learn (and still does), and would like to keep them
located either for future use or just in case I want to share
with anybody. None of it is in any specific order.
"""
    else:
        text = md.title(2, "Algunos recursos maravillosos")
        text += """\nLas siguientes listas corresponden a contenido que me ha 
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

    md.add(do_clickable(create_list(blogs), title=title_blogs))
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
