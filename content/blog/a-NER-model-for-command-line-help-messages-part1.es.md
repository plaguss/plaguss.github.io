---
title: "Un modelo NER para los mensajes de ayuda de las consolas (Parte 1: el programa en línea de comandos)"
date: 2023-02-21T18:55:27+01:00
draft: false
categories: ["NLP"]
tags: ["NLP", "NER", "spaCy", "Python", "rich"]
---

En esta serie de 3 partes voy a contar el viaje de crear un programa para detectar los diferentes
componentes/entidades del mensaje de ayuda de un programa por línea de comandos. Esta entrada
comenzará echando un vistazo al producto final [helpner](https://github.com/plaguss/helpner), un
programa escrito en python que se puede instalar desde [PyPI](https://pypi.org/project/helpner/),
la segunda parte tratará el flujo de trabajo de un pipeline en spaCy y finalmente echaremos un vistazo
a los datos de los que se alimentará spaCy para el modelo final.

> *Esta entrada asume algo de conocimiento de python, como instalar librerías de PyPI,*
> *y cierta familiaridad con spaCy.*

La siguiente imagen muestra la arquitectura de helpner, cada pieza está representada por un repostorio
de github diferente. Resaltado en amarillo en la parte inferior tenemos la parte correspondiente a [helpner](https://github.com/plaguss/helpner).

![helpner](/images/helpner-arch-part1.png)

### Que me llevó a empezar este proyecto?

Quería un proyecto de NLP para practicar algunas de las muchas facilidades que ofrece spaCy. De ser posible, el modelo debería ser fácil de usar por un usuario sin tener que crear una página web por simplicidad. Por otro lado, encontré [docopt](http://docopt.org/) de casualidad mientras exploraba librerías de python para crear CLIs. Resulta que esta librería y el fork de la misma que tiene mantenimiento ([docopt-ng](https://github.com/jazzband/docopt-ng)), pueden generar una CLI procesando un mensaje de ayuda escrito "apropiadamente" (vista el link previo para ver los ejemplos). Esta misma idea parecía una buena oportunidad.

> Se puede resolver este problema utilizando un modelo [NER](https://spacy.io/usage/linguistic-features#named-entities)? *...No me importa si no es el mejor enfoque*

Vamos a escribir un programa para la consola que pueda tomar un mensaje de ayuda de otro programa, y encontrar los diferentes elementos/entidades (comandos, argumentos y opciones) que lo conforman. Resulta que en alrededor de 200 lineas de código, podemos tener una primera versión prometedora :smile:. Está claro que no es tan sencillo internamente, pero spaCy hace que lo parezca.

### Entra helpner

Veamos como funciona [helpner](https://github.com/plaguss/helpner). La instalación consiste en dos pasos. Primero, instalamos con *pip* como es habitual, preferiblemente dentro de un *venv*. (Debería ser posible instalarlo utilizando [pipx](https://pypa.github.io/pipx/), pero no lo he probado todavía).

```console
$ pip install helpner
```

Este comando debería descargar la librería, pero en este momento esta incompleta, todavía debemos descargar el modelo que utiliza internamente. Para esto, se ofrece un comando conveniente (se puede visitar el README.md para más información):

```console
$ helpner download
```

Este proceso en dos pasos debería ser familiar a aquellos que ya conozcan [spaCy](https://spacy.io/). Utilizando este enfoque podemos separar el desarollo del modelo de el uso que hacemos del mismo. Podríamos actualizar el modelo de cualquier forma (por ejemplo reentrenarlo con datos distintos, o modificar el optimizador que utiliza), y solo necesitariamos actualizar el modelo (reejecutando el comando de descarga). Ocurre lo mismo con la librería, podemos añadir más funcionalidad sin necesidad de actualizar el modelo.

Ya estamos listos para utilizar *helpner* :collision:, veamos uno de los ejemplos de la documentación, como resaltar las entidades del de un mensaje de ayuda (este fue el primer caso de uso que se me vino a la mente).

```sh
flit install --help | helpner highlight
```

![flit-install-help](/images/flit-install-help.svg)

Para quien no conozca [flit](https://github.com/pypa/flit), es un programa por consola que simplifica empaquetar modulos de python. Este ejemplo muestra el mensaje de ayuda de uno de sus subcomandos, `flit install`. En la leyenda podemos ver que los posibles elementos o entidades son CMD (commandos o subcomandes, que en este caso depende de `flit` directamente), `ARG` (argumentos posicionales, que no aparecen en este caso) y `OPT` (argumentos opcionales, que corresponden a todos los elementos que están precedidos de uno o dos guiones, y el modelo ha predicho correctamente). Pero llaman la atención unas cuantas palabras al azar que salen resaltadas como si fueran `CMD`, que están claramente mal predichas. El modelo está lejos de ser perfecto, pero lo considero un éxito igualmente, los resultados parecen lo bastante prometedores!

¿Que ocurre por debajo? lo que hemos hecho ha sido mandar el mensaje de ayuda al modelo de *spaCy*, y hemos obtenido las predicciones:

```console
❯ flit install --help | helpner parse --no-json
{
    'install': ('CMD', 12, 19),
    '[-h]': ('OPT', 20, 24),
    '[-s]': ('OPT', 25, 29),
    '[--pth-file]': ('OPT', 30, 42),
    '[--user]': ('OPT', 43, 51),
    '[--env]': ('OPT', 52, 59),
    '[--python PYTHON]': ('OPT', 60, 77),
    '[--deps {all,production,develop,none}]': ('OPT', 98, 136),
    '[--only-deps]': ('OPT', 137, 150),
    '[--extras EXTRAS]': ('OPT', 171, 188),
    '-h, --help': ('OPT', 201, 211),
    'exit': ('CMD', 250, 254),
    '-s, --symlink': ('OPT', 257, 270),
    'package': ('CMD', 298, 305),
    '--pth-file': ('OPT', 373, 383),
    'module': ('CMD', 417, 423),
    '/': ('CMD', 423, 424),
    '--user': ('OPT', 497, 503),
    'local': ('CMD', 529, 534),
    '--env': ('OPT', 612, 617),
    '--python PYTHON': ('OPT', 749, 764),
    '--deps {all,production,develop,none}': ('OPT', 862, 898),
    '--only-deps': ('OPT', 1074, 1085),
    '--extras EXTRAS': ('OPT', 1192, 1207),
    'the': ('CMD', 1313, 1316),
    'ones': ('CMD', 1317, 1321),
    'implied': ('CMD', 1322, 1329),
    'by': ('CMD', 1330, 1332),
    'be': ('CMD', 1382, 1384),
    'useful': ('CMD', 1385, 1391)
}
```

Este output tiene toda la información necesaria para informar a `rich`. Las claves del diccionario corresponden a los elementos encontrados/predichos, y los valores contienen la entidad, comienzo y posición final de los "substrings". Con esta información, podemos hacer uso de [rich](https://rich.readthedocs.io/en/stable/introduction.html) para añadir algo de color a la consola.

Por supuesto, hay muchos errores (y este es un ejemplo que parece relativamente correcto), el modelo no puede predecir mejor que los datos de los que se ha alimentado. En otro post más adelante veremos como se obtienen los datos que alimentan este modelo.


