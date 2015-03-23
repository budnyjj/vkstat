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
(https://github.com/budnyjj/vkstat/blob/master/doc/pic/with_gephi.png)

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