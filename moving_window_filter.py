import numpy as np


def moving_window_filter(matrix, f, neighborhood_size):
    matrix_height, matrix_width = matrix.shape

    output_matrix = np.zeros([matrix_height - neighborhood_size + 1,
                              matrix_width - neighborhood_size + 1])

    for (row_num, col_num), value in np.ndenumerate(matrix):
        # Check if it already arrived at the right-hand edge as defined by the
        # size of the neighborhood box
        if not ((row_num > (matrix_height - neighborhood_size) or
                col_num > (matrix_width - neighborhood_size))):
            # Obtain each pixel component of an (n x n) 2-dimensional matrix
            # around the input pixel, where n equals neighborhood_size
            component_matrix = np.zeros([neighborhood_size, neighborhood_size])

            for row_offset in range(0, neighborhood_size):
                for column_offset in range(0, neighborhood_size):
                    component_matrix[row_offset][column_offset] = \
                        matrix[row_num + row_offset][col_num + column_offset]

            # Apply the transformation function f to the set of component
            # values obtained from the given neighborhood
            output_matrix[row_num, col_num] = f(component_matrix)

    return output_matrix
