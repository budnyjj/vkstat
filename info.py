#!/usr/sbin/python3
# -*- coding: utf-8 -*-

import argparse
import networkx as nx
import time

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

DESCRIPTION = 'Print characteristics of specified NetworkX graph'

if __name__ == '__main__':
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
    parser.add_argument("--genders", help="print profiles genders",
                    action="store_true")

    args = parser.parse_args()
    
    try:
        start_time = time.time()
    
        print("Load graph from {0}...".format(args.path))
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

        if args.periphery:
            print_periphery_nodes(nx.periphery(G), nodes_data)

        if args.degrees:
            print_degrees(G)

        # if args.genders:
        #     print_genders(G)

        gprint.print_elapsed_time(time.time() - start_time)
    except FileNotFoundError:
        print("Please, specify existing YAML source!")
    

