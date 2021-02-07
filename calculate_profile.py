from math import log
from collections import Counter


def entropy(probability_list):
    running_total = 0
    for item in probability_list:
        running_total += item * log(item, 2)

    if running_total != 0:
        running_total *= -1

    return running_total


def binary_entropy(p0, p1):
    return entropy([p0, p1])


def matrix_entropy(matrix):
    counts = dict(Counter(matrix.flatten())).values()
    total_count = sum(counts)
    discrete_dist = [float(x) / total_count for x in counts]
    return entropy(discrete_dist)


def profile(matrices):
    return [matrix_entropy(scale) for scale in matrices]
