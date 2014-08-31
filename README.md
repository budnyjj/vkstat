# vkstat
## overview

Collection of scripts for building and analyzing social graph based on vk.com API.
The social graph is a graph that depicts personal relations of internet users.
Users of the social network are presented as nodes, friendship relations between them -- as edges.

With a help of scripts from this collection you can build graphs based on data from vk.com,
process, analyze and plot them.

Here is the example of social graph built by these scripts:
![Example of social graph]
(https://github.com/budnyjj/vkstat/blob/master/examples/one.png)

## dependencies

These scripts written in **Python 3**, and has following external dependencies:
* [vkontakte3](https://github.com/budnyjj/vkontakte3) -- vk.com API for Python 3
* [networkx](https://networkx.github.io/) -- creation and manipulation of graph
* [matplotlib](http://matplotlib.org/) -- graph visualization

## scripts

* [get.py](https://github.com/budnyjj/vkstat/blob/master/get.py) -- use it for get data from vk.com.
  You can specify number of UIDs and set recursion level (get friends of friends). 
  It can use multiprocessing to speed-up download.

