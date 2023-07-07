---
title: "Pytokei, calling rust's tokei from python"
date: 2023-04-09T20:38:54+01:00
draft: false
categories: ["Python"]
tags: ["Python", "Rust"]
---

In this blog post I will walk through the steps I followed to start with rust, what resulted in [pytokei](https://github.com/plaguss/pytokei), a python wrapper of [tokei](https://github.com/XAMPPRocky/tokei/tree/master).

```console
❯ pytokei pytokei
                        pytokei                         
┏━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━┓
┃ language   ┃ Files ┃ Lines ┃ Code ┃ Comments ┃ Blanks ┃
┡━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━┩
│ Rust       │     9 │  1011 │  846 │       49 │    116 │
│ Python     │     5 │   568 │  436 │       13 │    119 │
│ Markdown   │    11 │   423 │  123 │      179 │    121 │
│ Plain Text │     4 │   133 │    0 │      133 │      0 │
│ TOML       │     3 │    75 │   59 │        6 │     10 │
│ YAML       │     1 │    69 │   63 │        0 │      6 │
│ Makefile   │     1 │    26 │   18 │        0 │      8 │
│ Dockerfile │     1 │    16 │    7 │        3 │      6 │
│ Shell      │     3 │    12 │   12 │        0 │      0 │
│ Autoconf   │     3 │     7 │    7 │        0 │      0 │
└────────────┴───────┴───────┴──────┴──────────┴────────┘
```

## Intro

After reading [Rust's book](https://doc.rust-lang.org/stable/book/), I was  looking for a excuse to build something in Rust. Just by taking a look at the book's index, one starts to wonder what to begin with...

Given that I'm comfortable enough with *python*, I tought it could be easy to 
write some bindings for a simple library already written in rust, so that I had some familiarity. By looking at [PyO3 examples](https://github.com/PyO3/pyo3#examples) I found a simple library that could help as a simple guide: [pyheck](https://github.com/kevinheavey/pyheck). Now its just a matter of finding a library to wrap.

To learn how to write bindings to rust from *python* its better for you to take a look at [maturin](https://www.maturin.rs/) and [PyO3](https://pyo3.rs/v0.19.1/class), here I just share my journey, but its not intented as a full guide to anything.

<!-- COMMENTS

- REF: https://www.peterbaumgartner.com/blog/wrapping-a-rust-crate-in-a-python-package/

Thanks to Maturin and PyO3 its so easy to mix the power of rust and the simplicity of Python.

- [PyO3 examples](https://github.com/PyO3/pyo3#examples)

-->


## Pytokei

Thinking about a good target library, I remembered a library I found [tokei](https://github.com/XAMPPRocky/tokei/tree/master) by chance some time ago. It seemed that exposing the public API to *python* should not be so hard.

### Tokei

From its readme:

``Tokei is a program that displays statistics about your code. Tokei will show the number of files, total lines within those files and code, comments, and blanks grouped by language.``

It is a simple command line program, but to expose to *python* what it does, we have to wrap as functions and or classes the contents of [lib.rs](https://github.com/XAMPPRocky/tokei/blob/master/src/lib.rs), we don't need anything about its CLI.

### Development

You can take a lookg at the [development](https://plaguss.github.io/pytokei/#development) section of pytokei's docs to get started. We just need to install [maturin](https://www.maturin.rs/) to create the package, and [PyO3](https://pyo3.rs/v0.19.1/) to create the bindings.

To package the code we need a [Cargo.toml](https://github.com/plaguss/pytokei/blob/main/Cargo.toml) for the rust and a [pyproject.toml](https://github.com/plaguss/pytokei/blob/main/pyproject.toml) for *python*, all of which is controlled by `maturin`.

So... I just want to mimic the behavior of `tokei`'s API, let's see what we need to implement for that end.

#### Rust

The public API of `pytokei` can be seen at the [lib.rs](https://github.com/plaguss/pytokei/blob/main/src/lib.rs) file. Lets take a look at what we will have visible from *python*:

```rust
#[pymodule]
fn _pytokei(_py: Python, m: &PyModule) -> PyResult<()> {
    let version = env!("CARGO_PKG_VERSION").to_string();
    m.add("__version__", version)?;
    m.add_class::<PyConfig>().unwrap();
    m.add_class::<PyLanguages>().unwrap();
    m.add_class::<PySort>().unwrap();
    m.add_function(wrap_pyfunction!(sort_types, m)?)?;
    m.add_class::<PyCodeStats>().unwrap();
    m.add_class::<PyReport>().unwrap();
    m.add_class::<PyLanguageType>().unwrap();
    m.add_class::<PyLanguage>().unwrap();
    Ok(())
}
```

We can read from the previous snippet that we have a module called `_pytokei`, along with some classes: `PyConfig`, `PyLanguages`... and a single function `sort_types`. How do they look like in *rust*?

Take a look at the implementation of the main class:

```rust
#[pyclass(name = "Languages")]
pub struct PyLanguages {
    pub languages: Languages,
}
```

Its just a wrapper of the `Languages` struct from `tokei`, with the *pyclass* attribute from PyO3 to make it a *python* class, which for this case works much like a *python* *decorator*.

Lets see now some of the methods:

```rust
#[pymethods]
impl PyLanguages {
    #[new]
    pub fn new() -> Self {
        PyLanguages {
            languages: Languages::new(),
        }
    }

    pub fn get_statistics(&mut self, paths: Vec<String>, ignored: Vec<String>, config: &PyConfig) {
        let paths_: Vec<&str> = paths.iter().map(String::as_str).collect();
        let paths_ = paths_.as_slice();

        let ignored_: Vec<&str> = ignored.iter().map(String::as_str).collect();
        let ignored_ = ignored_.as_slice();

        self.languages
            .get_statistics(&paths_, &ignored_, &config.config)
    }

    pub fn total(&self) -> PyLanguage {
        PyLanguage {
            language: self.languages.total(),
        }
    }

    pub fn language_names(&self) -> PyResult<Vec<&str>> {
        let vec = self
            .languages
            .iter()
            .map(|(lang_type, _)| lang_type.name())
            .collect();
        Ok(vec)
    }
...
```

It is just a matter of exposing the rust content to *python*, easy for this type of methods:

- `new`: Initializes the `PyLanguages` struct, does the job of the *python* constructor (`__init__`).

- `get_statistics`: It just parses the arguments to pass them to the `get_statistics` method from rust, doesn't return anything as the result is internally stored.

- `total`: Returns a `PyLanguage` in *python* with the result from an internal method.

- `language_names`: Creates and returns a *Vec* of *&str*, which is automatically translated by *PyO3* to a *list* of *str* in *python*.

We can practice rust one function at a time. For a simple case like this we just need to find how to expose the rust chunk of code to python, we don't need to get into nothing much complicated.

Let's see now the what the *python* version looks like.

#### Python API

From the *python* side, given the library is simple enough, we just have to write the type stubs in a .pyi file: [_pytokei.pyi](https://github.com/plaguss/pytokei/blob/main/pytokei/_pytokei.pyi) for our case. There we can see all *python* code, as well as the docstrings, deployed at [API docs](https://plaguss.github.io/pytokei/api/languages/).

The *python* interface to the `PyLanguage` struct from rust can be seen here:

```python
class Languages:
    """A class representing a list of languages counted in the provided directory.
    See [`LanguageType.list`](language_type.md)

    Examples
    --------
        ```python
        >>> from pytokei import Languages
        >>> langs = Languages()
        >>> langs
        Languages()
        ```

    References
    ----------
    [Languages implementation](https://docs.rs/tokei/latest/tokei/struct.Languages.html#impl)
    """

    def __init__(self) -> None: ...
    def get_statistics(
        self, paths: list[str], ignored: list[str], config: Config
    ) -> None:
        """Populates the Languages struct with statistics about languages provided by Language.

        Takes a list of of paths (as str) to recursively traverse, paths can be relative,
        absolute or glob paths.
        A second list of paths (as str) to ignore, these strings use the `.gitignore` syntax,
        such as `target` or `**/*.bk`.

        Parameters
        ----------
            paths : list[str]
                List of files to traverse. It may be a single directory.
            ignored : list[str]
                List of files to ignore. If you don't want anything ignored, just pass `["ignored"]`.
            config : Config
                Config instance. If you dont have any preferences, just pass `Config`.
        """
    def total(self) -> Language:
        """Summary of the Languages struct."""
    def language_names(self) -> Optional[list[str]]:
        """Returns the list of language names, if any was found."""
    ...
```

It doesn't contain the actual implementation, just the skeleton, enough for an IDE to help us with the autocompletion.

Lets see an example running `pytokei` against [pip](https://github.com/pypa/pip):

```python
$ python
>>> import pytokei
>>> from rich import print
>>> langs = pytokei.Languages()
>>> langs.get_statistics(["."], ["nothing"], pytokei.Config())
>>> print(langs.report_compact_plain())
{
    'TOML': {'blanks': 14, 'comments': 15, 'files': 17, 'lines': 162, 'code': 133},
    'ReStructuredText': {'comments': 0, 'files': 78, 'code': 7126, 'lines': 9702, 'blanks': 2576},
    'C': {'code': 0, 'comments': 0, 'blanks': 0, 'files': 1, 'lines': 0},
    'Markdown': {'blanks': 861, 'files': 27, 'comments': 2243, 'lines': 3408, 'code': 304},
    'PowerShell': {'files': 1, 'lines': 74, 'comments': 2, 'blanks': 11, 'code': 61},
    'Python': {'lines': 220272, 'files': 709, 'code': 188695, 'blanks': 22068, 'comments': 9509},
    'Autoconf': {'comments': 0, 'lines': 50, 'code': 44, 'blanks': 6, 'files': 10},
    'Plain Text': {'lines': 1293, 'files': 18, 'blanks': 96, 'code': 0, 'comments': 1197},
    'HTML': {'code': 77, 'comments': 0, 'blanks': 0, 'lines': 77, 'files': 11}
}
```

We are obtaining the statistics from the current working directory (in my case I was in the folder containing `pip`), we filter "nothing" (this is just a placeholder, no file or folder is called like that, so it works), and use the default `Config`, and we print the *compact report*, meaning we print the statistics at the language level.

You can see the equivalent example from `tokei` at [docs.rs](https://docs.rs/tokei/9.0.0/tokei/#examples). 

#### Python CLI

`pytokei` also exposes a *python* API and a cli which shows the results in the console similar to what `tokei` does, but using [rich](https://github.com/Textualize/rich). This is just an extra to mimic to obtain a similar command line interface to the one `tokei` gives us, but there is no more rust involved in this step.

The following block shows the result of running the program from the console against `pip`:

```bash
❯ pytokei pip                                                                          
                               pip                                
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┓
┃ language         ┃ Files ┃  Lines ┃   Code ┃ Comments ┃ Blanks ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━┩
│ Python           │   709 │ 220272 │ 188695 │     9509 │  22068 │
│ ReStructuredText │    78 │   9702 │   7126 │        0 │   2576 │
│ Markdown         │    27 │   3408 │    304 │     2243 │    861 │
│ Plain Text       │    18 │   1293 │      0 │     1197 │     96 │
│ TOML             │    17 │    162 │    133 │       15 │     14 │
│ HTML             │    11 │     77 │     77 │        0 │      0 │
│ PowerShell       │     1 │     74 │     61 │        2 │     11 │
│ Autoconf         │    10 │     50 │     44 │        0 │      6 │
│ C                │     1 │      0 │      0 │        0 │      0 │
└──────────────────┴───────┴────────┴────────┴──────────┴────────┘
```

## Conclusion

Its just a simple library, but it help me gain some confidence not only writing rust, but also reading an proper rust project, how to wrap it in python using *PyO3* and *maturin*, and upload the final result to [PyPI](https://pypi.org/project/pytokei/).

You can visit the github repository at [pytokei](https://github.com/plaguss/pytokei) as well as the [documentation](https://plaguss.github.io/pytokei/).
