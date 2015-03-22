# VKStat

Vkstat is a collection of scripts for building and analyzing social graph based
on Vkontakte (vk.com) API.
The social graph is a graph that depicts personal relations of internet users.
Users of the social network are presented as nodes,
friendship relations between them are presented as graph edges.

With a help of scripts from this collection you can build graphs based on
data from vk.com, process, analyze and plot them.

Here is the example of social graph built by these scripts (without data about individuals):
![Example of social graph]
(https://github.com/budnyjj/vkstat/blob/master/examples/with_gephi.svg)

In this graph, **node size** shows **total number friends in vkontakte network** --
the more common friends user has, the larger his node is.

The **node color** depends on **number of friends in graph** -- 
the more friends user has, the darker his node is.

The **edge color** depends on **position of the node** in graph: edges from central nodes are coloured in
red, while rest edges are coloured in yellow.

The **node label** contains basic information about profile.

## installation

These scripts are written in **Python 3** with some external dependencies:
* [vkontakte3](https://github.com/budnyjj/vkontakte3) --
vk.com API for Python 3 (required)
* [networkx](https://networkx.github.io/) --
graph creation and manipulation (required)
* [matplotlib](http://matplotlib.org/) --
graph visualization (required)
* [PyYAML](https://pypi.python.org/pypi/PyYAML) --
read/write graph from/to files in YAML format (optional)
* [PrettyTable](https://pypi.python.org/pypi/PrettyTable) --
print graph data in table format (optional)

## functionality overview

```bash
get.py --> process.py ---> plot.py
                       |
                       --> info.py
```

* [get.py](https://github.com/budnyjj/vkstat/blob/master/get.py) --
  use it for get data from vk.com.
  You can specify **number of UIDs** and set **recursion level**
  (get friends of friends). 
  It is possible to use **multiprocessing** to speed-up download.
  Built graph can be stored in **Pickle** or **YAML** format.

* [process.py](https://github.com/budnyjj/vkstat/blob/master/process.py) --
  use it to cut off nodes, which have small number of common neighbors in graph.
  It can be useful to **reduce graph size** 
  and/or **convert graph files between YAML and pickle formats**.

* [info.py](https://github.com/budnyjj/vkstat/blob/master/info.py) --
  use it to analyze obtained graph.
  Currently, this script can show graph **radius**, **diameter**,
  table of user parameters, such as
  **number of friends**, **number of followers**, **pagerank**, etc.

* [plot.py](https://github.com/budnyjj/vkstat/blob/master/plot.py) --
  use it to plot result graph.
  You can explore graph in interactive mode or write its representation to file 
  (**.png** or **.pdf** are currently supported). 
  For perfomance reasons, it is recommended to
  **plot graphs with less than 500 nodes**.

## ideas and bug reports

Send your ideas and bug reports/fixes to me: **budnyjj@pirates.by**.

# VKStat

VKStat -- это набор из скриптов, которые выполняют загрузку и обработку
социальных связей из популярной социальной сети [Вконтакте](https://vk.com).
Данные, загружаемые посредством VK API, представляются в виде 
[социального графа](https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%B3%D1%80%D0%B0%D1%84):
![Пример социального графа]
(https://github.com/budnyjj/vkstat/blob/master/examples/with_gephi.svg)

## установка

Эти скрипты написаны на **Python 3** со следующими внешними зависимостями:
* [vkontakte3](https://github.com/budnyjj/vkontakte3) --
VK API для Python 3 (обязательно)
* [networkx](https://networkx.github.io/) --
создание и обработка графов (обязательно)
* [PyYAML](https://pypi.python.org/pypi/PyYAML) --
чтение/запись графа в формате YAML (опционально)
* [PrettyTable](https://pypi.python.org/pypi/PrettyTable) --
печать данных графа в табличном виде (опционально)
* [matplotlib](http://matplotlib.org/) -- визуализация графа средствами Python
(опционально)
* [gephi](http://gephi.github.io/) -- визуализация графа средствами Gephi
(опционально)

## обзор функциональности

```bash
get.py --> process.py ---> plot.py
                       |
                       --> info.py
```

* [get.py](https://github.com/budnyjj/vkstat/blob/master/get.py) --
  используется для получения данных через VK API.
  Вы можете указать **несколько UID-ов пользователей**
  и установить **уровень рекурсии** (чтобы получать друзей друзей). 
  Для ускорения процесса загрузки можно использовать **мультипроцессинг**.

  Загруженный граф может быть сохранен в форматах  **Pickle** или **YAML**.

* [process.py](https://github.com/budnyjj/vkstat/blob/master/process.py) --
  используется для фильтрации узлов графа по различным признакам,
  а также конвертации графа между различными форматами.

* [info.py](https://github.com/budnyjj/vkstat/blob/master/info.py) --
  используется для табличного анализа содержимого графа.
  На данный момент, этот скрипт предоставляет данные о
  **радиусе** и **диаметре** графа,
  а также **число друзей**, **число фолловеров**, **pagerank**,
  и т. д.

* [plot.py](https://github.com/budnyjj/vkstat/blob/master/plot.py) --
  используется для отображения графа средствами matplotlib.
  Построенный граф может быть исследован интерактивно или сохранения
  в виде форматах png или pdf. 
  По причинам низкой производительности рекомендуется
  **строить графы размером не более 500 узлов**.
