# vkstat

Collection of scripts for building and analyzing social graph based on vk.com API.
The social graph is a graph that depicts personal relations of internet users.
Users of the social network are presented as nodes, friendship relations between them -- as edges.

With a help of scripts from this collection you can build graphs based on data from vk.com,
process, analyze and plot them.

Here is the example of social graph built by these scripts (without data about individuals):
![Example of social graph]
(https://github.com/budnyjj/vkstat/blob/master/examples/first.png)

In this graph, **node size** shows **total number friends in network** (not only common) --
the more common friends user has, the larger it is.

The **node color** depends on **number of common friends** (which is equal to node degree) -- 
the more friends user has, the darker it is. Nodes, which colored in yellow, 
have unknown total number of friends. 

The **edge color** depends on **position of the node** in graph: edges from central nodes are coloured in
red, while rest edges are coloured in yellow.

The **node label** contains information about profile (currently, it is user name, specified in profile).

## dependencies

These scripts has been written in **Python 3**, and has following external dependencies:
* [vkontakte3](https://github.com/budnyjj/vkontakte3) -- vk.com API for Python 3 (required)
* [networkx](https://networkx.github.io/) -- graph creation and manipulation (required)
* [matplotlib](http://matplotlib.org/) -- graph visualization (required)
* [PyYAML](https://pypi.python.org/pypi/PyYAML) -- read/write graph in YAML format (optional) 

## scripts

```bash
get.py --> process.py ---> plot.py
                       |
                       --> info.py
```

* [get.py](https://github.com/budnyjj/vkstat/blob/master/get.py) -- use it for get data from vk.com.
  You can specify **number of UIDs** and set **recursion level** (get friends of friends). 
  It is possible to use **multiprocessing** to speed-up download.

  Built graph can be stored in **Pickle** or **YAML** format (switch between them by output file extension).

* [process.py](https://github.com/budnyjj/vkstat/blob/master/process.py) -- use it to cut off 
  nodes, which have small number of common neighbors in graph. It can be useful to **reduce graph size** 
  and/or **convert graph files between YAML and pickle formats**.

* [info.py](https://github.com/budnyjj/vkstat/blob/master/info.py) -- use it to analyze obtained graph.
  Currently, this script can show graph **radius**, **diameter**, lists of **central** and **periphery nodes**,
  show **number of degrees per node**.

* [plot.py](https://github.com/budnyjj/vkstat/blob/master/plot.py) -- use it to plot result graph.
  You can explore graph in interactive mode or write its representation to file 
  (**.png** or **.pdf** are currently supported). 

  For perfomance reasons, I recommend you to **plot graphs with less than 500 nodes**.

## ideas and bug reports

Send your ideas and bug reports/fixes to me: **budnyjj@pirates.by**.
