# Various functions for printing various specific values
# in human-readable format

import sys
import time
import pprint

# pretty print object
pp = pprint.PrettyPrinter(indent=4)


def pretty_print(value):
    pp.pprint(value)

# print timedelta, provided in seconds,
# in human-readable format


def print_elapsed_time(timedelta):
    gm_timedelta = time.gmtime(timedelta)
    hours = int(time.strftime('%H', gm_timedelta))
    minutes = int(time.strftime('%M', gm_timedelta))
    seconds = int(time.strftime('%S', gm_timedelta))

    print('Total time elapsed: ', end='')
    if hours > 0:
        print('{0} hours, '.format(hours), end='')
    if minutes > 0:
        print('{0} minutes, '.format(minutes), end='')

    print('{0} seconds.'.format(seconds), end='')
    print()

# print progress bar in form: "[###-------]"


def print_progress(cur_value, max_value, width=72):
    progress = int((cur_value * 100) / max_value)

    # effective width -- width of bar without brackets
    e_width = width - 2

    # number of "#" in bar
    num_hashes = int((cur_value * e_width) / max_value)
    num_minuses = e_width - num_hashes

    sys.stdout.write('\r[{hashes}{minuses}] '
                     '{percentage}%'.format(hashes='#' * num_hashes,
                                            minuses='-' * num_minuses,
                                            percentage=progress))

    sys.stdout.flush()
