#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import time

try:
    import networkx as nx
except ImportError:
    print("This script requires NetworkX library to be installed.")
    exit(1)

import graph.io as io
import graph.printing as gprint

def precompute_node_data(graph):
    '''store information about nodes in dict keyed by UID'''
    data = {}
    for node in graph.nodes(data=True):
        data[node[0]] = node[1]
    return data

def print_central_nodes(nodes, nodes_data):
    '''print central nodes (the eccentricity 
    of each of these nodes is equal to radius)'''
    if len(nodes) == 1:
        central_node = nodes[0]
        print("The central node is: {0} ({first_name} " \
              "{last_name})".format(central_node,
                                    **nodes_data[central_node]))
    else:
        print("There are {0} central nodes:".format(len(nodes)))
        for node in nodes:
            print(" {0}\t({first_name} " \
                  "{last_name})".format(node, **nodes_data[node]))
    print()

def print_periphery_nodes(nodes, nodes_data):
    '''print central nodes (the eccentricity 
    of each of these nodes is equal to diameter)'''
    if len(nodes) == 1:
        periphery_node = nodes[0]
        print("The periphery node is: {0} ({first_name} " \
              "{last_name})".format(periphery_node,
                                    **nodes_data[periphery_node]))
    else:
        print("There are {0} periphery nodes:".format(len(nodes)))
        for node in nodes:
            print(" {0}\t({first_name} " \
                  "{last_name})".format(node, **nodes_data[node]))
    print()

def print_degrees(graph):
    '''pretty print node degrees'''

    def sort_by_degree(node):
        return node[1]['degree']

    nodes = graph.nodes(data=True)
    for node in nodes:
        node[1]['degree'] = graph.degree(node[0])

    nodes.sort(key = sort_by_degree, reverse=True)

    print("{:<49}{:10}".format("Node", "Degree"))
    for node in nodes:
        node_name = "{} {} ({})".format(node[1]['first_name'], 
                                        node[1]['last_name'],
                                        node[0])
        print("{:<50}{:5}".format(node_name, node[1]['degree']))
    print()

def print_num_friends(graph):
    '''pretty print node number of friends (and followers, if exists)'''
    INF = 99999

    def sort_by_friends_total(node):
        return node[1]['friends_total']

    def sort_by_followers_per_friends(node):
        return node[1]['followers_per_friends']

    # collect nodes only with 'friends_total'
    nodes = []
    for node in graph.nodes(data=True):
        if (('friends_total' in node[1]) and
            (node[1]['friends_total'] > 0)):
            nodes.append(node)

    for node in nodes:
        node[1]['is_activist'] = ''
        if 'followers_total' not in node[1]:
            node[1]['followers_total'] = 0
            node[1]['followers_per_friends'] = 0
        else:
            followers_per_friends = node[1]['followers_total'] / node[1]['friends_total']
            node[1]['followers_per_friends'] = node[1]['followers_total'] / node[1]['friends_total']

            if ((node[1]['friends_total'] > 500) and (followers_per_friends < 0.2)):
                node[1]['is_activist'] = 'Yes'

    nodes.sort(key = sort_by_friends_total, reverse=True)

    print("{:<40}{:15}{:15}{:10}{:15}".format("Node", "Friends", 
                                              "Followers", "Fl/Fr", "Is Activist?"))
    for node in nodes:        
        node_name = "{} {} ({})".format(node[1]['first_name'], 
                                        node[1]['last_name'],
                                        node[0])
        print("{:<40}{:<15}{:<15}{:<10.4f}{:<15}".format(node_name, 
                                                         node[1]['friends_total'], 
                                                         node[1]['followers_total'],
                                                         node[1]['followers_per_friends'],
                                                         node[1]['is_activist']))
    print()

def print_pagerank(graph):
    def sort_by_pagerank(pair_uid_pagerank):
        return pair_uid_pagerank[1]
    
    print("{:<40}{:15}".format("Node", "Pagerank"))

    pageranks = nx.pagerank(graph).items()
    for uid, pagerank in sorted(pageranks, key=sort_by_pagerank, reverse=True):
        node_name = "{} {} ({})".format(graph.node[uid]['first_name'],
                                        graph.node[uid]['last_name'],
                                        uid)
        print("{:<40}{:<10.4f}".format(node_name, pagerank))

    print()
    
DESCRIPTION = 'Print characteristics of specified NetworkX graph'

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('path', metavar='PATH', type=str,
                    help='path to YAML file which contains graph data')
parser.add_argument("-r", "--radius", help="calculate graph radius",
                    action="store_true")
parser.add_argument("-d", "--diameter", help="calculate graph diameter",
                    action="store_true")
parser.add_argument("--central", help="print central nodes",
                    action="store_true")
parser.add_argument("--periphery", help="print periphery nodes",
                    action="store_true")
parser.add_argument("--degrees", help="print node degrees",
                    action="store_true")
parser.add_argument("--num-friends", help="print total number friends (and followers)",
                    action="store_true")
parser.add_argument("--pagerank", help="print pagerank",
                    action="store_true")
parser.add_argument("--pagerank", help="print pagerank",
                        action="store_true")
    
args = parser.parse_args()
    
try:
    start_time = time.time()
    
    G = io.read_graph(args.path)
    
    print("Precompute data structures...")

try:
    start_time = time.time()

    G = io.read_graph(args.path)

    print("Precompute data structures...")

    # nodes_data = {'uid': {'attr1': 'val1', ...}}
    nodes_data = precompute_node_data(G)

    print("Calculate required values...\n")        

    print(nx.info(G), "\n")

    if args.radius:
        print("Graph radius: {0}\n".format(nx.radius(G)))
    
    if args.central:
        print_central_nodes(nx.center(G), nodes_data)

    if args.diameter:
        print("Graph diameter: {0}\n".format(nx.diameter(G)))

    if args.pagerank:
        print_page_rank(G)
    
    if args.periphery:
        print_periphery_nodes(nx.periphery(G), nodes_data)

    # table values
    if args.degrees:
        print_degrees(G)

    if args.num_friends:
        print_num_friends(G)

    if args.pagerank:
        print_pagerank(G)
        
except FileNotFoundError:
    print("No such file or directory! Quitting...")
except IOError:
    print("IOError happened! Quitting...")
else:
    gprint.print_elapsed_time(time.time() - start_time)    

