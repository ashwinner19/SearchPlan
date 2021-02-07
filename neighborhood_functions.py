import numpy as np


def avg_components(component_matrix):
    running_total = 0
    num_components = 0

    for (row_num, col_num), value in np.ndenumerate(component_matrix):
        running_total += value
        num_components += 1

    output_value = running_total / num_components

    return output_value
