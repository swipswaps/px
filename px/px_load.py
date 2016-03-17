"""Functions for visualizing system load over time in a Unicode graph"""

import os


def get_load_string():
    avg0to1, avg1to5, avg5to15 = get_load_values()
    recent, between, old, peak = averages_to_levels(avg0to1, avg1to5, avg5to15)
    graph = levels_to_graph([old] * 15 + [between] * 4 + [recent])
    return graph + " (scale 0-{})".format(peak)


def average_to_level(average, peak):
    level = 4 * (average / peak)
    return int(round(level))


def averages_to_levels(avg0, avg1, avg2):
    """
    Converts three load averages into three levels.

    A level is a 0-4 integer value.

    This function returns the three leves, plus the peak value the levels are
    based on.
    """
    peak = max(avg0, avg1, avg2)
    if peak < 1.0:
        peak = 1.0

    l0 = average_to_level(avg0, peak)
    l1 = average_to_level(avg1, peak)
    l2 = average_to_level(avg2, peak)
    return (l0, l1, l2, peak)


def levels_to_graph(levels):
    """
    Convert an array of levels into a unicode string graph.

    Each level in the levels array is an integer 0-4.

    The returned string will contain two levels per rune.
    """
    return None


def get_load_values():
    """
    Returns three system load numbers:
    * The first is the average system load over the last 0m-1m
    * The second is the average system load over the last 1m-5m
    * The third is the average system load over the last 5m-15m
    """
    avg1, avg5, avg15 = os.getloadavg()

    avg0to1 = avg1
    avg1to5 = (5 * avg5 - avg1) / 4.0
    avg5to15 = (15 * avg15 - 5 * avg5) / 10.0

    return (avg0to1, avg1to5, avg5to15)