#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time
import math

try:
    import networkx as nx
except ImportError:
    print('This script requires NetworkX to be installed.')
    exit(1)

import graph.io as io
import utils.print as gprint

DESCRIPTION = 'Plot NetworkX graph which specified in YAML file'


def assign_labels(graph):
    '''create dict with human-readable labels, assigned to nodes'''
    labels = {}
    for node in graph.nodes_iter(data=True):
        try:
            labels[node[0]] = '{first_name} {last_name}'.format(**node[1])
        except KeyError as e:
            print('There is no such data attribute: {0}'
                  ' in {1}'.format(e, node[0]))
    return labels


def assign_node_colors(graph):
    """assign colors to nodes by number of friends contained in graph."""
    colors = []
    for node in graph.nodes_iter():
        node_color = math.log(1 + graph.degree(node))
        colors.append(node_color)
    return colors


def assign_node_sizes(graph, default_size=100, default_scale=25):
    """assign node sizes by total number of friends in whole network."""
    sizes = []
    for node in graph.nodes_iter(data=True):
        try:
            node_size = node[1]['friends_total'] / default_scale
            node_size += 1
            node_size *= default_size
            sizes.append(node_size)
        except (KeyError, ValueError):
            sizes.append(1)
    return sizes


def assign_edge_colors(graph):
    """Highlight edges from central nodes."""
    color_list = []
    try:
        central_nodes = set(nx.center(G))
    except nx.exception.NetworkXError:
        for edge in G.edges_iter():
            color_list.append('y')
    else:
        for edge in G.edges_iter():
            if ((edge[0] in central_nodes) or
                    (edge[1] in central_nodes)):
                color_list.append('r')
            else:
                color_list.append('y')

    return color_list

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('path', metavar='SOURCE', type=str,
                    help='path to file which contains graph data.')
parser.add_argument('-o', '--output', type=str,
                    help='path to file for writing plot image')
parser.add_argument('--with-latex', action='store_true',
                    help='use LaTeX for text processing')
parser.add_argument('--no-labels', action='store_true',
                    help='draw graph without labels')
parser.add_argument('--dpi', type=int, help='set dpi')

args = parser.parse_args()

try:
    # configure pyplot before import
    if args.with_latex:
        from matplotlib import rc
        rc('font', **{'family': 'sans-serif', 'sans-serif': ['Monospace']})
        rc('text', usetex=True)
        rc('text.latex', unicode=True)
        rc('text.latex', preamble='\\usepackage[utf8]{inputenc}')
        rc('text.latex', preamble='\\usepackage[russian]{babel}')

    import matplotlib.pyplot as plt
    plt.switch_backend('GTK3Cairo')
except ImportError:
    print('Matplotlib, gobject and cairo are required to run this script.')

try:
    start_time = time.time()
    G = io.read_graph((args.path))

    nx.draw(G,
            labels=assign_labels(G),
            with_labels=not args.no_labels,
            cmap=plt.cm.YlOrRd,
            node_size=assign_node_sizes(G),
            node_color=assign_node_colors(G),
            edge_color=assign_edge_colors(G),
            )

    if args.output:
        # store plot to file
        plt.savefig(args.output, dpi=args.dpi)
        gprint.print_elapsed_time(time.time() - start_time)
    else:
        # interactive drawing
        gprint.print_elapsed_time(time.time() - start_time)
        plt.show()
except FileNotFoundError:
    print('No such file or directory! Quitting...')
except IOError:
    print('IOError happened! Quitting...')
