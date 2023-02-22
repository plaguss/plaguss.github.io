---
title: "A NER Model for Command Line Help Messages (Part 1: The console program)"
date: 2023-02-21T18:55:27+01:00
draft: true
---

This 3 part series will tell the journey of creating a program to detect the different components
of a command line program's help message. We will start by looking at the final product, [helpner](https://github.com/plaguss/helpner), a python program that can be installed from [PyPI](https://pypi.org/project/helpner/).

#### *Helpner architecture*
![helpner](/images/helpner-arch-part1.png)

What led me to start this project?

- I wanted an NLP problem which could be tackled using [spaCy](URL).
- Also, the model should be simple/small enough to be run in the console.

I found [docopt](http://docopt.org/) by chance, and it seemed like a good excuse to try
a similar objective but using neural networks, just for the sake of it :smile:.

> Can we solve this using a Named Entity Recognition model? *...even if its not the best approach*

Lets try to write a CLI program that can take a help message from another
CLI program, and find the different elements (`commands`, `arguments` and `options`)
which form it. It turns out that in around 200 lines of code, we can have a viable
first approach. Of course, this is not that simple, but with spaCy it feels like it.
