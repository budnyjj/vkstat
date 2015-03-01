"""This module contains various predicate functions."""

import graph.stats as stats

def is_media_activist(node, avg_num_friends):
    '''Check, if person is media-activist.
    Media-activist is a person, who:
    1. has number of friends more than 5 * average number of friends
    or
    2. has number of friends more than 2 * average number of friends and
    number of his friends is more than 5 * number of his followers.'''
    hard_limit = avg_num_friends * 3
    soft_limit = avg_num_friends * 2
    soft_ff_ratio = 5
    hard_ff_ratio = 10

    if 'friends_total' in node[1]:
        num_friends = node[1]['friends_total']
        if (num_friends > hard_limit):
            return True        
        elif 'followers_total' in node[1]:
            num_followers = node[1]['followers_total']
            if num_followers > hard_limit:
                return True
            elif ((num_followers > soft_limit) and
                (num_followers > num_friends * soft_ff_ratio)):
                return True
            elif num_friends > num_followers * hard_ff_ratio:
                return True
            elif ((num_friends > soft_limit) and
                (num_friends > num_followers * soft_ff_ratio)):
                return True
            
    return False

