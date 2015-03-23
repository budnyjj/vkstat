# VKStat

Vkstat is a collection of scripts for building and analyzing social graph
from [Vkontakte(https://vk.com) social network.
The social graph is a graph that depicts personal relations of internet users.
Users of the social network are presented as nodes,
friendship relations between them are presented as graph edges.

Here is the example of social graph built by these scripts (without data about individuals):
![Example of social graph]
(https://github.com/budnyjj/vkstat/blob/master/doc/pic/clusterization.png)

See more nice pictures [here]
(https://github.com/budnyjj/vkstat/blob/master/doc/RU/plot.md).

## Installation

To run VKStat, yuo should **install dependencies**, and then
clone this repo.
You can check functionality of any of these scripts by this command:

```bash
./get.py --help
```

If you see list of available parameters, then it works correctly :)

### Dependencies

VKStat is written in **Python 3** with some external dependencies:

#### Required

* [vkontakte3](https://github.com/budnyjj/vkontakte3) --
vk.com API for Python 3
* [networkx](https://networkx.github.io/) --
graph creation and manipulation

#### Optional 
* [PyYAML](https://pypi.python.org/pypi/PyYAML) --
read/write graph from/to files in YAML format
* [PrettyTable](https://pypi.python.org/pypi/PrettyTable) --
print graph data in table format (info.py)
* [matplotlib](http://matplotlib.org/) --
graph visualization with Python (plot.py)
* [Gephi](http://gephi.github.io/) --
graph visualization with Gephi

## Functionality overview

In general, work process with graph can be represented in this form:

```bash
get.py --> process.py ---> info.py
                       |
                       --> plot.py
                (GEXF) |
                       --> Gephi
```

* [get.py](https://github.com/budnyjj/vkstat/blob/master/get.py) --
  use it for get data from vk.com.
  You can specify **number of UIDs** and set **recursion level**
  (get friends of friends). 
  It is possible to use **multiprocessing** to speed-up download.

  Built graph can be stored in various formats.

* [process.py](https://github.com/budnyjj/vkstat/blob/master/process.py) --
  use it to cut off nodes, which have small number of common neighbors in graph.
  It can be useful to **reduce graph size** 
  and/or **convert graph files between different formats**.

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

* [Gephi](http://gephi.github.io/) --
  use it to plot result graph.
 
  Gephi is a more powerful tool for graph visualization,
  and allows to **represent graphs up to 2500 nodes** with the same hardware requirements,
  as with **plot.py**.

  Gephi use its own format GEXF, so you should convert your social
  graph to it with **process.py**.
