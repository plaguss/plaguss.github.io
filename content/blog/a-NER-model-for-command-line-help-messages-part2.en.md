---
title: "A NER Model for Command Line Help Messages (Part 2: spaCy projects to the rescue)"
date: 2023-03-14T21:01:11+01:00
draft: true
categories: ["NLP"]
tags: ["NLP", "NER", "spaCy", "Python"]
---

Lets continue our journey with [helpner-core](https://github.com/plaguss/helpner-core), the [spaCy project](https://github.com/explosion/projects) that does all the magic behind `helpner`.

![helpner-core](/images/helpner-arch-part2.png)

This repository contains a spaCy template for a NER model, and allows to build the end-to-end spaCy workflow from the [`spacy project`](https://spacy.io/api/cli#project) cli command manager. In short, spaCy projects present *End-to-end NLP workflows from prototype to production*. 

We will visit the different steps of the whole workflow following the commands that involve the pipeline.

## `helpner-core` workflow

All this process is stored in the [`project.yml`](https://github.com/plaguss/helpner-core/blob/main/project.yml) file, which contains the single source of truth for the project.

#### Dataset creation

![helpner-core](/images/helpner2/workflow_1.png)

The first step is the dataset creation. I could have gone down the path of gathering a different number of CLI help messages and start labelling them, but it could easily get a very tedious task, and as the task allowed it, I started implementing a synthetic data generator (I will present [cli-help-maker](https://github.com/plaguss/cli-help-maker) in a different post).

Lets introduce the first command:

```console
spacy project run create-dataset
```

Running this command calls the program [cli-help-maker](https://github.com/plaguss/cli-help-maker), with a [`dataset.yaml`](https://github.com/plaguss/helpner-core/blob/main/assets/v0.2.0/dataset.yaml) file which contains the arguments needed for the program. This simplifies the versioning of the different data sets, we just have to store the *yaml* of any given version, all the relevant information to create a dataset is contained in a single file. Other than that the dataset contains random data with the layout and content we want the model to capture.

This command returns two files:

- `dataset.jsonl`: A [jsonl](https://jsonlines.org/) file, where each line corresponds to a sample, that contains *message* and the *annotations*.

```json
{"message":"Usage: \n    chedlock digynia borofluoric begirdle underbeadle [-d] [CONGRUENTLY...] [ACROBATISM... [ZONOID...]]\n\nFusillade preventively hogyard approachles.\n\nCommands:\n    digynia\n...", "annotations": [["CMD",21,28],["CMD", 29,40]...] }
{"message": "usage: \n    sterelmintha hearth --hydromorphic-beethovian -g --titanical -e ODONTOLCATE-\n...", "annotations":[["CMD",25,31],["OPT",32,57]...]}
...
```

- `arguments.jsonl`: Another `jsonl` file not used for during the program. We keep in this file the arguments that were used to generate each CLI help message, just for further analysis, to know what to expect from each dataset.

```json
{"indent_spaces":4.0,"total_width":120.0,...}
{"indent_spaces":4.0,"total_width":78.0,...}
```

Now we are ready to prepare the dataset for the training process.

### Data workflow

The process is divided in two different worflows just to outline the fact that the first part corresponds to data preparation, training and evaluation, while the next part deals with packaging related processes.

#### Data preparation

![helpner-core](/images/helpner2/workflow_2.png)


This step involves two different scripts:

- [`split.py`](https://github.com/plaguss/helpner-core/blob/main/scripts/split.py), which is run by the following program:

```console
spacy project run split
```

This command simply splits the file in two different files `dataset_train.jsonl` and `dataset_dev.jsonl` with a random partition of 80/20. Given the dataset is generated randomly, there is no need for more complicated strategies.

- [`convert.py`](https://github.com/plaguss/helpner-core/blob/main/scripts/convert.py), run by the following program:

```console
spacy project run convert
```

It transforms the *message* in each row of the `jsonl` file to a serializable format: [`DocBin`](https://spacy.io/api/docbin/), to obtain two new files `dataset_train.spacy` and `dataset_dev.spacy`.

Its time for some action!

#### Training

![helpner-core](/images/helpner2/workflow_3.png)


The following program starts the training process:

```console
spacy project run train
```

This command reads all the necessary info from the [config files](https://github.com/plaguss/helpner-core/tree/main/configs) (you can read more in the spaCy [training docs](https://spacy.io/usage/training#quickstart)), which correspond to the NER *components*, CPU *hardware* and *optimized for* efficiency.

Its created from the spaCy defaults, there is no need to change anything during this step. Given the model is just a proof of concept, and the dataset used is small enough, we can just train in our personal computer without a GPU, it just needs some minutes to finish the training process.

After this step has finished, we are left with a directory containing our named entity recognition model.

#### Evaluation

![helpner-core](/images/helpner2/workflow_4.png)

After running the [`benchmark accuracy`](https://spacy.io/api/cli#benchmark-accuracy) command we can inspect the model results on the *development* dataset. There should exist a different dataset to test the results, but for simplicity, the results are reported on this dataset, and the model is finally run against some help messages from real CLI apps (watch the `helpner` readme).

```console
spacy project run evaluate
```

The output file of the command is a `metrics.json` file that contains information about the model's performance (this content can be transferred to a README file easily as we will see later). The following table presents the information per entity, **NER per type table:**

|  | P | R | F |
| --- | --- | --- | --- |
| CMD | 98.25 | 99.96 | 99.10 |
| ARG | 94.79 | 89.97 | 92.32 |
| OPT | 98.88 | 98.96 | 98.92 |

The first thing to note is that the results seem to be really good for such a simple model with no special meaning besides the layout of the entities. The smallest value corresponds to the *recall* (R) value of `ARG` entities (89.97), the element that tends to get more confused, while the highest corresponds to the *recall* of `CMD`.

*But*, this results must be taken carefully, the dataset in which the model was trained is totaly synthetic, and the results may not be as good as expected in real data. *It just shows that the model is able to learn from the data it was fed with.*


### Packaging workflow

Up to this point, we run the enabled workflows in `project.yml` file, which correspond to:

```console
spacy project run all
```

Those are related to the data processing, model training and evaluation. A second workflow (more a subsequent set of commands) is for house keeping related tasks:

#### Packaging

![helpner-core](/images/helpner2/workflow_5.png)

The first of these commands is the [`package`](https://spacy.io/api/cli#package). SpaCy easily allows to generate a package automatically from our model, just by running a command, so it can be easily installed and loaded afterwards:

```console
spacy project run package
```

Just place the contents generated somewhere accessible to pip, and you are ready to `pip install` the model to be used with spaCy. It even comes with a README.md file generated from the metrics.json file obtained, so the relevant content is autoexplained.

Following the spaCy approach to model storage with [spaCy models](https://github.com/explosion/spacy-models), the trained models are stored in the [releases](https://github.com/plaguss/helpner-core/releases) of the repository, and `helpner` deals with the installation process via `pip install`.

#### Readme

![helpner-core](/images/helpner2/workflow_6.png)

One last command and we are finished!

SpaCy templates come with another magic command to generate a pretty README.md for your project: [`spacy project document`](https://spacy.io/api/cli#project-document). I wanted to add some more content automatically to this README file, and with a little script and the help of [`wasabi`](https://github.com/explosion/wasabi) (a Explosion library which helps with console printing, but also with Markdown rendering), its as simple as it gets:


```console
spacy project run readme
```

This command generates the readme for the `helpner-core` repository automatically, adding to the original generated README some additional metrics, like information from the dataset used for the current version, which seemed interesting enough to be added.

#### Deployment

![helpner-core](/images/helpner2/workflow_7.png)

The most relevant step make the model available for everybody easily isn't properly mapped to a command, I have to do it manually for the moment :grin:.

But lets assume the following command is already working (*for the moment, this is done using GitHub in the browser directly*):

```console
spacy project run release
```

The previously created package is uploaded to github as a release (the [releases](https://github.com/plaguss/helpner-core/releases) can be seen in the following page), including a small description of the model's accuracy, the weights and the necessary information to import the model just like any other spaCy model, after installation, it can be imported as usual in spaCy:

```python
import spacy
nlp = spacy.load("en_helpner_core")
```

And just like we would do with any other spaCy model, we can pass text to it. As te expected input for the model are command line help messages, [`helpner`](https://github.com/plaguss/helpner) helps dealing with the content directly on the shell.

## Conclusion

In this post we followed workflow outlined in [`helpner-core`](https://github.com/plaguss/helpner-core). We leveraged the power of spaCy project template to train, evaluate, and deploy a Named Entity Recognition model which can be `pip install`ed as a dependency to run as any spaCy model. Feels amazing to deal with an end to end NLP pipeline with just a few command line programs.
