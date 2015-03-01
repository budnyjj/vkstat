#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time

try:
    import networkx as nx
except ImportError:
    print("This script requires NetworkX to be installed.")
    exit(1)

import graph.io as io
import graph.stats as stats
import graph.predicates as predicates

import utils.print as gprint

DESCRIPTION = 'Load NX graph from SOURCE, ' \
              'process, and save it to DESTINATION.'

DEFAULT_TRIM = 1

def trim(graph, min_num_nodes):
    '''Return copy of graph with only nodes with
    number of edges greater, than min_num_nodes'''
    
    print('Trim nodes with less than {0} ' \
          'connected edges:'.format(min_num_nodes))

    # make copy of graph to count neighbors per node
    res_graph = graph.copy()

    # get start number of nodes to show progress
    start_num_nodes = graph.number_of_nodes()

    for n,node in enumerate(graph.nodes()):
        gprint.print_progress(n+1, start_num_nodes)
        if graph.degree(node) < min_num_nodes:
            res_graph.remove_node(node)

    # need to add newline after progress bar
    print('\n')
    return res_graph

def exclude_media_activists(graph):
    '''Exclude "media-activists" from graph.'''

    print('Exclude media-activists:')

    avg_friends = stats.avg_num_friends(graph)

    # make copy of graph to count neighbors per node
    res_graph = graph.copy()

    # get start number of nodes to show progress
    start_num_nodes = graph.number_of_nodes()

    for n,node in enumerate(graph.nodes(data=True)):
        gprint.print_progress(n+1, start_num_nodes)
        if predicates.is_media_activist(node, avg_friends):
            res_graph.remove_node(node[0])

    # need to add newline after progress bar
    print('\n')
    return res_graph

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('src', metavar='SOURCE', type=str,
                        help='source file with graph data')
    parser.add_argument('dst', metavar='DESTINATION', type=str,
                        help='destination file')
    parser.add_argument("--exclude-media-activists",
                        help="exclude media-activists from graph",
                        action="store_true")
    parser.add_argument("--exclude-alone",
                        help="exclude not connected nodes from graph",
                        action="store_true")
    parser.add_argument('--trim', metavar='N', type=int,
                        default=DEFAULT_TRIM, help='trim nodes with' \
                        'less than N connected edges')
    args = parser.parse_args()

    start_time = time.time()

    try:
        G = io.read_graph(args.src)

        print("Graph stats before requested operations:")
        print(nx.info(G), "\n")

        if args.exclude_media_activists:
            G = exclude_media_activists(G)

        if args.trim > DEFAULT_TRIM:
            G = trim(G, args.trim)

        if args.exclude_alone:
            G = trim(G, 1)

        print("Graph stats after requested operations:")
        print(nx.info(G), "\n")

        io.write_graph(G, args.dst)
    except FileNotFoundError:
        print("No such file or directory! Quitting...")
    except IOError:
        print("IOError happened! Quitting...")
    else:
        gprint.print_elapsed_time(time.time() - start_time)




