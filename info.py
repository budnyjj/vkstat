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

        # end of table
        if cur_index == -1:
            return table_str
        
    return table_str[:cur_index+1] + first_line

def avg_num_friends(graph):
    '''Average number of friends in graph'''
    num_nodes = 0
    num_friends = 0
    for node in graph.nodes(data=True):
        if 'friends_total' in node[1]:
            num_friends += node[1]['friends_total']
            num_nodes += 1
    
    if num_nodes == 0:
        return 0
    else:
        return num_friends / num_nodes


def avg_num_followers(graph):
    '''Average number of followers in graph'''
    num_nodes = 0
    num_followers = 0
    for node in graph.nodes(data=True):
        if 'followers_total' in node[1]:
            num_followers += node[1]['followers_total']
            num_nodes += 1
    
    if num_nodes == 0:
        return 0
    else:
        return num_followers / num_nodes
        

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

def append_media_activist(graph, table_data):
    '''Append information about "media-activism". '''

    avg_friends = avg_num_friends(graph)
    high_threshold_friends = avg_friends * 3
    low_threshold_followers = high_threshold_friends / 3

    print("High friends:", high_threshold_friends) 
    print("Low followers:", low_threshold_followers)
    
    # first, setup all values to false
    for node in graph.nodes(data=True):
        node_name = gen_username(node[1]['first_name'],
                                 node[1]['last_name'],
                                 node[0])
        is_activist = ""
        if (('friends_total' in node[1]) and ('followers_total' in node[1])):
            if ((node[1]['friends_total'] > high_threshold_friends) and
                (node[1]['followers_total'] < low_threshold_followers)):
                is_activist = "True"

        if node_name in table_data:
            table_data[node_name].append(is_activist)
        else:
            table_data[node_name] = [ is_activist ]
    
# list of implemented fields
impl_fields = [
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
    {
        "header" : "media-activist",
        "function" : append_media_activist,
        "align" : "c"
    },
]
            
DESCRIPTION = 'Print characteristics of specified NetworkX graph'

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('path', metavar='PATH', type=str,
                    help='path to YAML file which contains graph data')
parser.add_argument("-i", "--info",
                    help="print general information about graph",
                    action="store_true")
parser.add_argument("-r", "--radius", help="print graph radius",
                    action="store_true")
parser.add_argument("-d", "--diameter", help="print graph diameter",
                    action="store_true")

parser.add_argument("--avg-friends", help="print average number of friends",
                    action="store_true")
parser.add_argument("--avg-followers", help="print average number of followers",
                    action="store_true")

impl_headers = ",".join([field["header"] for field in impl_fields])
parser.add_argument("-f", "--fields", metavar='FIELDS', type=str,
                    help="print specified fields of each node:\n"\
                    "{}".format(impl_headers))
parser.add_argument("-s", "--sort", metavar='FIELD', type=str,
                    help="sort by FIELD from specified FIELDS")
parser.add_argument('-t', '--top', metavar='NUM_USERS', type=int,
                    help='print only top NUM_USERS')

args = parser.parse_args()

try:
    start_time = time.time()

    G = io.read_graph(args.path)
    
    if args.info:
        print(nx.info(G), "\n")

    if args.radius:
        print("Graph radius: {0}\n".format(nx.radius(G)))

    if args.diameter:
        print("Graph diameter: {0}\n".format(nx.diameter(G)))

    if args.avg_friends:
        print("Average number of friends: {0}\n".format(avg_num_friends(G)))

    if args.avg_followers:
        print("Average number of followers: {0}\n".format(avg_num_followers(G)))
        
    if args.fields:
        try:
            from prettytable import PrettyTable
        except ImportError:
            print("This script requires PrettyTable library to be installed.")
            exit(1)

        args_fields = args.fields.split(",")

        for i, field in enumerate(args_fields):
            args_fields[i] = field.lower().strip()
        
        table_headers = [ "Username" ]
        table_align = {"Username": "l"}
        table_data = {}

        for field in impl_fields:
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

