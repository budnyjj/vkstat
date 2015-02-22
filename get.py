#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time
import functools
import random
from multiprocessing import Pool
import cProfile, pstats

try:
    import networkx as nx
except ImportError:
    print("This script requires NetworkX to be installed.")
    exit(1)

try:
    import vkontakte
except ImportError:
    print("This script requires vkontakte package to be installed.")
    print("Download and install it from https://github.com/budnyjj/vkontakte3")  
    exit(1)

import graph.io as io
import utils.print as gprint

def write_time_profiling_data(profiler, filename):
    '''Write time profiling data to file.'''
    ps = pstats.Stats(profiler)
    print("Write time profiling information " \
          "to: {0}.\n".format(filename))
    ps.dump_stats(filename)

def args_are_valid(args):
    '''Validate cli arguments. Raise ValueError if they are not correct.'''
    if args.recursion_level <= 0:
        print("Recursion level should be greater than zero!\n")
        raise ValueError
    elif args.pool_size <= 0:
        print("Pool size should be greater than zero!\n")
        raise ValueError
    else:
        print("Provided arguments are seem to be correct...\n")
 
def get_profile(uid, req_fields = 'first_name, last_name, sex',
                max_err_count = 5):
    '''Get information (profile) about user with specified uid.'''
    answer = None
    error_count = 0

    # max value of sleep time
    max_time_to_sleep = 10
    # used to delay request with errors
    time_to_sleep = random.uniform(1, 2)

    while True:
        try:
            # get only first element of list 
            answer = VK.getProfiles(uids = uid,
                                    fields = req_fields)[0]
        except vkontakte.VKError as e:
            print('E: profile {}:'.format(uid))
            if e.code == 6:
                error_count += 1
                print('   Vk.com bandwith limitations. ', end='')
                if error_count <= max_err_count:
                    print('Now try again (#{})...'.format(error_count))
                    # Need to sleep due to vk.com bandwidth limitations
                    time.sleep(time_to_sleep)

                    if time_to_sleep <= max_time_to_sleep:
                        # exponentially increase time_to_sleep
                        time_to_sleep *= 2
                else:
                    print('Reached maximal bandwith error count ({0})! '\
                          'Skip...'.format(error_count))
                    return []
            else:
                print('   {}.'.format(e.description))
                return []

        except Exception as e:
            print('E: profile {}:'.format(uid))
            print('   {}.'.format(e))
            return []

        else:
            print('S: profile {uid}: ' \
                  '{first_name} {last_name}.'.format(**answer))
            return answer

def get_friends(profile, req_fields = 'first_name, last_name, sex', 
                max_err_count = 5):
    '''Get list with friend profiles of user with specified profile'''
    answer = None
    error_count = 0
    # used to delay request with errors
    time_to_sleep = random.uniform(0.1, 0.2)

    while True:
        try:
            # get only first element of list 
            answer = VK.friends.get(uid = profile['uid'],
                                    fields = req_fields)
        except vkontakte.VKError as e:
            print('E: friends of {uid} '\
                  '({first_name} {last_name}):'.format(**profile))
            if e.code == 6: # bandwith limitations
                error_count += 1
                print('   Vk.com bandwith limitations. ', end='')
                if error_count <= max_err_count:
                    print('Try again (#{0})...'.format(error_count))
                    # Need to sleep due to vk.com bandwidth limitations
                    time.sleep(time_to_sleep)
                    # exponentially increase time_to_sleep
                    time_to_sleep *= 2
                else:
                    print('   Reached maximal bandwith error count ({0})! '\
                          'Skip...'.format(error_count))
                    return []

            else:
                print('   {}.'.format(e.description))
                return []

        except Exception as e: # unknown error occured 
            print('E: friends of {uid} '\
                  '({first_name} {last_name}):'.format(**profile))
            print('   {}.'.format(e))
            return []

        else: # got friends without errors
            print('S: {number} friends of {uid}: ' \
                  '({first_name} {last_name}).'.format(
                      number = len(answer), **profile))
            return answer

def get_num_followers(uid, max_err_count = 5):
    '''Get number of followers of user with specified UID.
    Return -1 if cannot do so. '''
    answer = None
    error_count = 0
    # used to delay request with errors
    time_to_sleep = random.uniform(0.1, 0.2)

    while True:
        try:
            answer = VK.subscriptions.getFollowers(uid = uid,
                                                   count = 0)['count']
        except vkontakte.VKError as e:
            print('E: followers of {}:'.format(uid))
            if e.code == 6:
                error_count += 1
                print('   Vk.com bandwith limitations. ', end='')
                if error_count <= max_err_count:
                    print('Now try again (#{})...'.format(error_count))
                    # Need to sleep due to vk.com bandwidth limitations
                    time.sleep(time_to_sleep)
                    # exponentially increase time_to_sleep
                    time_to_sleep *= 2
                else:
                    print('Reached maximal bandwith error count ({0})! '\
                          'Skip...'.format(error_count))
                    return -1
            else:
                print('   {}.'.format(e.description))
                return -1

        except Exception as e:
            print('E: followers of {}:'.format(uid))
            print('   {}.'.format(e))
            return -1
        else:
            print('S: user {} has {} followers.'.format(uid, answer))
            return answer

def strip_attributes(node, preserve_attrs):
    '''Strip unnecessary data attributes from node'''
    node_attrs = list(node[1].keys())
    for attr in node_attrs:
        if attr not in preserve_attrs:
            del node[1][attr]
    return node

def profile_to_node(src_profile):
    '''convert source profile to graph node'''
    return (src_profile['uid'], src_profile)

def build_edges(src_profile, dst_profiles):
    '''create set of edges, compatible with NX graph format'''
    edges = set()
    for dst_profile in dst_profiles:
        edges.add( (src_profile['uid'], dst_profile['uid']) )
    return edges

def construct_graph(uids, required_attributes = ('first_name',
                                                 'last_name',
                                                 'sex'),
                    with_num_followers = False,
                    max_recursion_level = 1, pool_size = 1,
                    time_profiler = None):
    '''get and build graph data for specified uids'''

    # get list of profiles using get_profile() in multiple processes
    def _get_init_profiles(uids, attrs_string):
        print("Get init profiles...\n")

        # get_profile() with required data attributes
        req_get_profile = functools.partial(get_profile,
                                            req_fields=attrs_string)

        init_profiles = []

        if pool_size == 1:
            # no need to organize pool
            init_profiles = list(map(req_get_profile, uids))
        else:
            # disable profiling, because of new fork processes
            if time_profiler:
                time_profiler.disable()
            # organize multiprocessing calculations
            with Pool(processes=pool_size) as pool:
                init_profiles = list(pool.map(req_get_profile, uids))
            # enable profiling
            if time_profiler:
                time_profiler.enable()

        return init_profiles

    # get list of friend profiles, indexed by init_profiles,
    # using get_friends() in multiple processes
    def _get_friend_profiles(init_profiles, attrs_string):
        # get_friends() with required data attributes
        req_get_friends = functools.partial(get_friends,
                                            req_fields=attrs_string)

        friend_profiles = []

        if pool_size == 1:
            # no need to organize pool
            friend_profiles = list(map(req_get_friends,
                                       init_profiles))
        else:
            # disable profiling, because of new fork processes
            if time_profiler:
                time_profiler.disable()
            # organize multiprocess calculations
            with Pool(processes=pool_size) as pool:
                friend_profiles = list(pool.map(req_get_friends,
                                                init_profiles))
            # enable profiling
            if time_profiler:
                time_profiler.enable()

        print("\nThere are {0} obtained friend profiles on current level " \
              "of recursion.\n".format(sum(map(len, friend_profiles))))

        return friend_profiles

    # get information about user (node) followers and append it to nodes
    # using get_num_followers in multiple processes
    def _get_num_followers(nodes):
        # full list of user uids
        all_uids = [node[0] for node in nodes]

        # uids of users with 'friends_total' 
        uids_with_friends_total = [node[0] for node in nodes if 'friends_total' in node[1]]

        # list of user uids, contains only nodes with 'friends_total'
        num_followers_per_uid = []

        if pool_size == 1:
            # no need to organize pool
            num_followers_per_uid = list(map(get_num_followers, uids_with_friends_total))
        else:
            # disable profiling, because of new fork processes
            if time_profiler:
                time_profiler.disable()

            # organize multiprocess calculations
            with Pool(processes=pool_size) as pool:
                num_followers_per_uid = list(pool.map(get_num_followers,
                                                      uids_with_friends_total))
            # enable profiling
            if time_profiler:
                time_profiler.enable()

        # append number of followers to nodes
        for i,num_followers in enumerate(num_followers_per_uid):
            if num_followers >= 0:
                # quick and dirty solution
                req_index = all_uids.index(all_uids[i])
                nodes[req_index][1]['followers_total'] = num_followers

    # convert list of lists to list
    def _flatten(list_of_lists):
        return [e for l in list_of_lists for e in l]

    # append information about number of friends
    # it cannot be multiprocessed for unknown reasons
    def _append_num_friends(init_profiles, friend_profiles):
        for i, init_profile in enumerate(init_profiles):
            init_profile['friends_total'] = len(friend_profiles[i])

    # append only NEW nodes from src_list to dst_list
    # without duplicates and cut data
    def _append_nodes(src_list, dst_list):
        # UID: index of node with UID in dst_list
        dst_node_indexes = { node[0]: i for i,node in enumerate(dst_list) }

        for node in src_list:
            # check, 
            # if uid of source node not in list of destination uids,
            if node[0] not in dst_node_indexes:
                dst_list.append(node)
                dst_node_indexes[node[0]] = len(dst_list) - 1
            # if there is total number of friends in node,
            # then this node is newer,
            # so we need to replace older node by this
            elif 'friends_total' in node[1]:
                # replace node in dst_list with actual data    
                dst_list[dst_node_indexes[node[0]]] = node
            
    # strip unnecessary attributes using strip_attributes(),
    # but preserve 'friends_total' and multiprocessing capabilities
    def _strip_attributes(nodes, preserve_attrs):
        # convert to list
        mod_attrs = list(preserve_attrs)
        # append 'friends_total' to preserve this attribute
        mod_attrs.append('friends_total')
        # convert back to tuple
        mod_attrs = tuple(mod_attrs)

        # strip_attributes() with required data attributes
        req_strip_attributes = functools.partial(strip_attributes,
                                                 preserve_attrs=mod_attrs)

        if pool_size == 1:
            # no need to organize pool
            nodes[:] = map(req_strip_attributes, nodes)
        else:
            # disable profiling, because of new fork processes
            if time_profiler:
                time_profiler.disable()
                # organize multiprocess calculations
                with Pool(processes=pool_size) as pool:
                    nodes[:] = pool.map(req_strip_attributes, nodes)
            # enable profiling
            if time_profiler:
                time_profiler.enable()

        return nodes
    
    # Enable profiling
    if time_profiler:
        time_profiler.enable()

    # Current level of recursion
    cur_level = 0

    # Contains all data required to build graph
    gd_accumulator = { 'nodes' : [], 'edges' : set() }
    
    # Build required attributes string. 
    req_attrs_string = ', '.join(required_attributes)

    # List of user profiles with requested UIDs, for example
    # init_profiles = [{
    #     'first_name' : 'Roman',
    #     'last_name' : 'Budny',
    #     'uid' : 55358627 }, ...]
    init_profiles = _get_init_profiles(args.uids, req_attrs_string)

    while cur_level < max_recursion_level:
        print("\nGet friend profiles...")
        print("Current level of recursion is {0}.\n".format(cur_level))

        # list of friends of users, which specified in init_profiles
        friend_profiles = _get_friend_profiles(init_profiles, req_attrs_string)

        # append information about total number of friends to
        # profiles in init_profiles
        _append_num_friends(init_profiles, friend_profiles) 

        print("Merge obtained friend profiles into graph data...\n")
        # temporary storage for nodes and edges, use it 
        # because of optimization purpouses
        all_obtained_nodes = []
        all_obtained_edges = set()

        # iterate by init list of profile 
        for i, init_profile in enumerate(init_profiles):
            all_obtained_edges.update(build_edges(init_profile,
                                                  friend_profiles[i]))

            all_obtained_nodes.extend(map(profile_to_node, friend_profiles[i]))
            all_obtained_nodes.append(profile_to_node(init_profile))

        # append obtained data to graph data accumulator
        _append_nodes(all_obtained_nodes, gd_accumulator['nodes'])
        gd_accumulator['edges'].update(all_obtained_edges)

        init_profiles = _flatten(friend_profiles)

        # disable profiling
        if time_profiler:
            time_profiler.disable()

        cur_level += 1

    # Enable profiling
    if time_profiler:
        time_profiler.enable()

    _strip_attributes(gd_accumulator['nodes'], required_attributes)

    # Get number of followers
    if with_num_followers:
        print("Get number of followers per user...\n")
        _get_num_followers(gd_accumulator['nodes'])

    print("\nBuild graph with obtained data...\n")
    graph = nx.Graph()

    graph.add_nodes_from(gd_accumulator['nodes'])
    graph.add_edges_from(gd_accumulator['edges'])

    # Disable profiling
    if time_profiler:
        time_profiler.disable()

    return graph


DESCRIPTION = 'Get information about friends of user ' \
              'with specified UID in social network vk.com'

TOKEN_VK = '2e27464b84d9a9833248daa69ac07ec4e9ef98a05' \
           '1ad62dd18dc4a51513281a8de4249170a575d40f1332'

VK = vkontakte.API(token = TOKEN_VK)

DEFAULT_ATTRIBUTES = [ 'first_name', 'last_name', 'sex' ]

time_profiler = None

if __name__ == '__main__':
    # set cli options
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('uids', metavar='UID', type=int, nargs='+',
                        help='UID of vk.com user.')
    parser.add_argument('-w', '--write-to', metavar='PATH', type=str,
                        required=True,
                        help='file to write graph data. ' \
                        'It currently supports YAML and pickle formats, '
                        'swithing between them by extension.')
    parser.add_argument('-p', '--pool-size', metavar='N', type=int,
                        default=1, help='number of downloading '
                        'threads in pool.')
    parser.add_argument('-r', '--recursion-level', metavar='N', type=int,
                        default=1, help='recursion deepness, ' \
                        'use it to get friends of friends, etc.')
    parser.add_argument('--data-attributes', metavar='ATTR', type=str,
                        nargs='+', default=DEFAULT_ATTRIBUTES,
                        help='attributes for requesting from vk.com')
    parser.add_argument('--with-num-followers', action='store_true',
                        help='get number of followers per user')
    parser.add_argument('--time-profiling', metavar='PATH', type=str,
                        help='write speed profile in pStats' \
                        'compatible format to file, specified by PATH')

    # parse cli options
    args = parser.parse_args()

    try:
        args_are_valid(args)
        start_time = time.time()
        
        if args.time_profiling:
            time_profiler = cProfile.Profile()

        print("Start constructing graph for vk.com users with UIDs:",
              ", ".join(map(str, args.uids)))
        print("Requested data attributes:", ", ".join(args.data_attributes))
        print("Recursion level:", args.recursion_level)
        print("Pool size:", args.pool_size, "\n")
       
        G = construct_graph(uids = args.uids,
                            required_attributes = tuple(args.data_attributes),
                            with_num_followers = args.with_num_followers,
                            max_recursion_level = args.recursion_level,
                            pool_size = args.pool_size,
                            time_profiler = time_profiler)
        
        print(nx.info(G), "\n")
        
        io.write_graph(G, args.write_to)

        if args.time_profiling:
            write_time_profiling_data(time_profiler, args.time_profiling)

    except ValueError:
        print("ValueError happened! Quitting...")
    except IOError:
        print("IOError happened! Quitting...")
    else:
        gprint.print_elapsed_time(time.time() - start_time)
