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

try:
    from prettytable import PrettyTable
except ImportError:
    print("This script requires prettytable library to be installed.")
    exit(1)
    
import graph.io as io
import utils.print as gprint


def gen_username(first_name, last_name, uid):
    return "{} {} ({})".format(first_name, last_name, uid)

def add_rows(table_data, table):
    for username in table_data:
        table_data[username].insert(0, username)
        table.add_row(table_data[username])

def top_table(table_str, num_newlines):
    first_index = table_str.find("\n")
    first_line  = table_str[:first_index+1]
    
    cur_index = 0
    for _ in range(num_newlines + 3):
        cur_index = table_str.find("\n", cur_index+1)
    
    return table_str[:cur_index+1] + first_line


def append_central_nodes(graph, table_data):
    '''Append periphery nodes to table_data'''

    # first, setup all values to false
    for node in graph.nodes(data=True):
        node_name = gen_username(node[1]['first_name'],
                                 node[1]['last_name'],
                                 node[0])
        if node_name in table_data:
            table_data[node_name].append("")
        else:
            table_data[node_name] = [ "" ]

    # second, update these values to True for periphery 
    for uid in nx.center(graph):
        node_name = gen_username(graph.node[uid]['first_name'],
                                 graph.node[uid]['last_name'],
                                 uid)
        table_data[node_name][-1] = "True"


def append_periphery_nodes(graph, table_data):
    '''Append periphery nodes to table_data'''

    # first, setup all values to false
    for node in graph.nodes(data=True):
        node_name = gen_username(node[1]['first_name'],
                                 node[1]['last_name'],
                                 node[0])
        if node_name in table_data:
            table_data[node_name].append("")
        else:
            table_data[node_name] = [ "" ]

    # second, update these values to True for periphery 
    for uid in nx.periphery(graph):
        node_name = gen_username(graph.node[uid]['first_name'],
                                 graph.node[uid]['last_name'],
                                 uid)
        table_data[node_name][-1] = "True"


def append_degree(graph, table_data):
    '''Append degree of each node to table_data'''

    for node in graph.nodes(data=True):
        node_name = gen_username(node[1]['first_name'],
                                 node[1]['last_name'],
                                 node[0])
        node_degree = graph.degree(node[0])
        if node_name in table_data:
            table_data[node_name].append(node_degree)
        else:
            table_data[node_name] = [ node_degree ]

        
def append_num_friends(graph, table_data):
    '''Append number of friends (and followers, if exists)
    of each node to table_data'''

    # collect nodes only with 'friends_total'
    for node in graph.nodes(data=True):
        node_name = gen_username(node[1]['first_name'],
                                 node[1]['last_name'],
                                 node[0])

        if 'friends_total' in node[1]:
            num_friends = node[1]['friends_total']
        else:
            num_friends = 0

        if node_name in table_data:
            table_data[node_name].append(num_friends)
        else:
            table_data[node_name] = [ num_friends ]

def append_num_followers(graph, table_data):
    '''Append number of friends (and followers, if exists) of each node to table_data'''

    # collect nodes only with 'friends_total'
    for node in graph.nodes(data=True):
        node_name = gen_username(node[1]['first_name'],
                                 node[1]['last_name'],
                                 node[0])

        if 'followers_total' in node[1]:
            num_friends = node[1]['followers_total']
        else:
            num_friends = 0

        if node_name in table_data:
            table_data[node_name].append(num_friends)
        else:
            table_data[node_name] = [ num_friends ]
            
def append_pagerank(graph, table_data):
    pageranks = nx.pagerank(graph).items()
    for uid, pagerank in pageranks:
        node_name = gen_username(graph.node[uid]['first_name'],
                                 graph.node[uid]['last_name'],
                                 uid)
        if node_name in table_data:
            table_data[node_name].append(pagerank)
        else:
            table_data[node_name] = [ pagerank ]
    
DESCRIPTION = 'Print characteristics of specified NetworkX graph'

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('path', metavar='PATH', type=str,
                    help='path to YAML file which contains graph data')
parser.add_argument("-i", "--info",
                    help="print general information about graph",
                    action="store_true")
parser.add_argument("-r", "--radius", help="calculate graph radius",
                    action="store_true")
parser.add_argument("-d", "--diameter", help="calculate graph diameter",
                    action="store_true")
parser.add_argument("-f", "--fields", metavar='FIELDS', type=str,
                    help="comma-separated list of FIELDS to show, "\
                    "for example:\n central,periphery,degree,"\
                    "friends,followers,pagerank")
parser.add_argument("-s", "--sort", metavar='FIELD', type=str,
                    help="sort by FIELD from FIELDS")
parser.add_argument('-t', '--top', metavar='NUM_LINES', type=int,
                    help='print only top NUM_LINES')

args = parser.parse_args()

try:
    start_time = time.time()

    G = io.read_graph(args.path)

    print("Compute requested values")
    
    if args.info:
        print(nx.info(G), "\n")

    if args.radius:
        print("Graph radius: {0}\n".format(nx.radius(G)))

    if args.diameter:
        print("Graph diameter: {0}\n".format(nx.diameter(G)))

    if args.fields:
        args_fields = args.fields.split(",")

        for i, field in enumerate(args_fields):
            args_fields[i] = field.lower().strip()

        fields = [
            {
                "header" : "degree",
                "function" : append_degree,
                "align" : "r"
            },
            {
                "header" : "friends",
                "function" : append_num_friends,
                "align" : "r"
            },
            {
                "header" : "followers",
                "function" : append_num_followers,
                "align" : "r"
            },
            {
                "header" : "pagerank",
                "function" : append_pagerank,
                "align" : "r"
            },
            {
                "header" : "central",
                "function" : append_central_nodes,
                "align" : "c"
            },
            {
                "header" : "periphery",
                "function" : append_periphery_nodes,
                "align" : "c"
            },
        ]
        
        table_headers = [ "Username" ]
        table_align = {"Username": "l"}
        table_data = {}

        for field in fields:
            if field["header"] in args_fields:
                col_header = field["header"].capitalize()
                table_headers.append(col_header)
                col_function = field["function"]
                col_function(G, table_data)
                table_align[col_header] = field["align"]
        
        table = PrettyTable(table_headers)
        add_rows(table_data, table)
    
        # set align
        for col_header in table_align:
            table.align[col_header] = table_align[col_header]
    
        table.float_format = "5.5"
    
        if args.sort:
            args_sort = args.sort.capitalize()
            if args_sort in table_headers:
                table.sortby = args_sort
                table.reversesort = True
            else:
                print("Please, specify correct field to sort on:\n",
                      ", ".join(table_headers))
                exit(1)

        table_str = str(table)
        if args.top:
            table_str = top_table(table_str, args.top)
            
        print(table_str)

except FileNotFoundError:
    print("No such file or directory! Quitting...")
except IOError:
    print("IOError happened! Quitting...")
else:
    gprint.print_elapsed_time(time.time() - start_time)    

