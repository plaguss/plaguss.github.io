---
title: Home
linkTitle: Home
menu: main
weight: 3
---


## Projects

- [`talking-python`](https://github.com/plaguss/talking-python): Streamlit app to explore [talk python to me](https://talkpython.fm/episodes/all)
podcast episodes using semantic search.
It grabs all the episodes transcriptions weekly, creates embeddings from them and 
stores them in a `chroma` vector database to allow searching for them using natural language.
The app is deployed at [explore-talk-python-to-me](https://explore-talk-python-to-me.streamlit.app/).
        
- [`translate_md`](https://github.com/plaguss/translate-md/blob/main/pyproject.toml): A client to translate markdwon files from english to spanish,
makes use of [spanglish](https://github.com/plaguss/spanglish) for the translation service, a Ray app that serves a 🤗 Transformer model.
- [`helpner`](https://github.com/plaguss/helpner): A python console program to extract entities from command line 
programs' help messages. It makes use of two intermediate libraries: [`helpner-core`](https://github.com/plaguss/helpner-core) as a
spaCy template, and [`cli-help-maker`](https://github.com/plaguss/cli-help-maker) as a data generator.
- `MoViNets for CrossFit`: A plotly dash app to classify CrossFit movements _(no longer)_ 
deployed to AWS, based on a finetuned version of [Mobile Video Networks (MoViNets)](https://github.com/tensorflow/models/tree/master/official/projects/movinet), the tensorflow implementation of 
a network to classify human movements in videoclips. The repos still need to be better
organized, but los entre los comopnentes, a helper library can be seen here: [movinets_helper](https://github.com/plaguss/movinets_helper), the 
code for the front here: [movinets_dash_app](https://github.com/plaguss/movinets_dash_app), and here the pieces related to the cloud: [lambda_aws](https://github.com/plaguss/tfm-misc/tree/main/lambda_aws).

- [`pytokei`](https://github.com/plaguss/pytokei): Python bindings to [tokei](https://github.com/XAMPPRocky/tokei), 
a rust program to extract statistics from your code.
- [`biblioteca-cidaen`](https://github.com/plaguss/biblioteca-cidaen): _(written in spanish)_. A prototype for an 'online library' where the students could
share their master's thesis.
Even though its tailored for the master's program that I coursed, 
it can be used as an interesting approach to introduce students
to collaboration in GitHub and the Pull Request mecanism.

## Some wonderful resources
The following lists of items correspond to content that has
helped me to learn (and still does), and would like to keep them
located either for future use or just in case I want to share
with anybody. None of it is in any specific order.


{{< rawhtml >}}
 <details>
<summary> 📔 Blogs I tend to visit from time to time:</summary> 
{{< /rawhtml >}}

- [https://snarky.ca/](https://snarky.ca/)
- [https://pradyunsg.me/blog/](https://pradyunsg.me/blog/)
- [https://textual.textualize.io/blog/](https://textual.textualize.io/blog/)
- [https://explosion.ai/blog](https://explosion.ai/blog)
- [https://ljvmiranda921.github.io](https://ljvmiranda921.github.io)
- [https://www.peterbaumgartner.com/blog/](https://www.peterbaumgartner.com/blog/)
- [https://stackoverflow.blog/](https://stackoverflow.blog/)
- [https://github.blog/](https://github.blog/)
- [https://lucumr.pocoo.org/](https://lucumr.pocoo.org/)
- [https://netflixtechblog.com/](https://netflixtechblog.com/)
- [https://wandb.ai/site/articles](https://wandb.ai/site/articles)
- [https://huggingface.co/blog](https://huggingface.co/blog)
- [https://blog.ganssle.io/](https://blog.ganssle.io/)
- [https://pytorch.org/blog/](https://pytorch.org/blog/)
- [https://www.anyscale.com/blog](https://www.anyscale.com/blog)
- [https://simonwillison.net/](https://simonwillison.net/)
- [https://lilianweng.github.io](https://lilianweng.github.io)
- [https://jalammar.github.io/](https://jalammar.github.io/)
- [https://alvarobartt.github.io/](https://alvarobartt.github.io/)
- [https://koaning.io/](https://koaning.io/)
- [https://thomwolf.io/](https://thomwolf.io/)
- [https://hynek.me/articles/](https://hynek.me/articles/)

{{< rawhtml >}}
 </details>
 
{{< /rawhtml >}}

{{< rawhtml >}}
 <details>
<summary> 📻 Podcasts I listen:</summary> 
{{< /rawhtml >}}

- [The Stack Overflow Podcast](https://stackoverflow.blog/podcast/)
- [Podcast.__init__](https://www.pythonpodcast.com/)
- [The Machine Learning Podcast](https://www.themachinelearningpodcast.com/)
- [Data Engineering Podcast](https://www.dataengineeringpodcast.com/)
- [The Real Python Podcast](https://realpython.com/podcasts/rpp/)
- [The Changelog](https://changelog.com/podcast)
- [Test & Code in Python](https://testandcode.com/)
- [Talk Python To Me](https://talkpython.fm/)
- [The Rustacean Station Podcast](https://rustacean-station.org/)
- [Python Bytes](https://pythonbytes.fm/)
- [Practical AI](https://changelog.com/practicalai)
- [Open Source Startup Podcast](https://podcasts.google.com/search/Open%20Source%20Startup%20Podcast)
- [MLOps.community](https://podcast.mlops.community/)
- [Gradient Dissent](https://podcast.wandb.com/)

{{< rawhtml >}}
 </details>
 
{{< /rawhtml >}}

{{< rawhtml >}}
 <details>
<summary> 📚 Books I have read (completely or some parts), or that are waiting to be read:</summary> 
{{< /rawhtml >}}

- [Natural Language Processing with PyTorch: Build Intelligent Language Applications Using Deep Learning](https://www.amazon.com/Natural-Language-Processing-PyTorch-Applications/dp/1491978236)
- [Natural Language Processing with Transformers](https://www.oreilly.com/library/view/natural-language-processing/9781098136789/)
- [Building Data Science Applications with FastAPI](https://www.oreilly.com/library/view/building-data-science/9781801079211/)
- [Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/)
- [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)
- [Building Machine Learning Systems with Python](https://www.amazon.com/Building-Machine-Learning-Systems-Python/dp/1782161406)
- [High Performance Python](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
- [Fluent Python](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/)
- [Python for Data Analysis](https://www.oreilly.com/library/view/python-for-data/9781449323592/)
- [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
- [Big Data and Machine Learning in Quantitative Investment](https://www.amazon.com/Data-Machine-Learning-Quantitative-Investment/dp/1119522226)
- [Programming: Principles and Practice Using C++](https://www.amazon.com/Programming-Principles-Practice-Using-C-ebook/dp/B00KPTEH8C?ref_=ast_author_dp)
- [Cython](https://www.oreilly.com/library/view/cython/9781491901731/)
- [Mastering Object-Oriented Python](https://www.oreilly.com/library/view/mastering-object-oriented-python/9781789531367/)
- [Clean Code: A Handbook of Agile Software Craftsmanship](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Feature Engineering for Machine Learning](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/)
- [Hands-On Machine Learning with Scikit-Learn]( Keras)
- [Web Scraping with Python](https://www.oreilly.com/library/view/web-scraping-with/9781491985564/)
- [CPython Internals](https://realpython.com/products/cpython-internals-book/)

{{< rawhtml >}}
 </details>
 
{{< /rawhtml >}}