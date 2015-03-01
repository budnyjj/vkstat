"""Graph-related statistical functions"""

import networkx as nx

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
