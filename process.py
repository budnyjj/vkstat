#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time

try:
    import networkx as nx
except ImportError:
    print("NetworkX is required to run this script.")

import graph.io as io
import graph.printing as gprint

DESCRIPTION = 'Load NX graph from SOURCE, ' \
              'process, and save it to DESTINATION.'

DEFAULT_TRIM = 1

# return trimmed copy of graph
def trim(graph, min_num_nodes):
    print('Trim nodes with less than {0} ' \
          'connected edges:'.format(min_num_nodes))

    # make copy of graph to count neighbors per node
    res_graph = graph.copy()

    # get start number of nodes to show progress
    start_num_nodes = graph.number_of_nodes()

    for n,node in enumerate(graph.nodes()):
        gprint.print_progress(n+1, start_num_nodes)
        if len(graph.neighbors(node)) < min_num_nodes:
            res_graph.remove_node(node)

    # need to add newline after progress bar
    print('\n')
    return res_graph

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('src', metavar='SOURCE', type=str,
                        help='source file with graph data')
    parser.add_argument('dst', metavar='DESTINATION', type=str,
                        help='destination file')
    parser.add_argument('--trim', metavar='N', type=int,
                        default=DEFAULT_TRIM, help='trim nodes with' \
                        'less than N connected edges')
    args = parser.parse_args()

    start_time = time.time()

    try:
        G = io.read_graph(args.src)

        print("Graph stats before requested operations:")
        print(nx.info(G), "\n")

        if args.trim != DEFAULT_TRIM:
            G = trim(G, args.trim)

        print("Graph stats after requested operations:")
        print(nx.info(G), "\n")
            
        io.write_graph(G, args.dst)
    except FileNotFoundError:
        print("No such file or directory! Quitting...")
    except IOError:
        print("IOError happened! Quitting...")
    else:
        gprint.print_elapsed_time(time.time() - start_time)




