import numpy as np
import re


def count_arr_matches(arr: np.ndarray):
    return len(re.findall("XMAS", "".join(arr))) + len(re.findall("SAMX", "".join(arr)))


def count_xmas_matches(matrix: np.ndarray) -> int:
    count = 0

    # Rows
    for i in range(matrix.shape[0]):
        count += count_arr_matches(matrix[i, :])

    # Cols
    for j in range(matrix.shape[1]):
        count += count_arr_matches(matrix[:, j])

    # Diagonals top-left to bottom-right
    for k in range(-matrix.shape[0], matrix.shape[1]):
        count += count_arr_matches(matrix.diagonal(offset=k))

    # Diagonals bottom-left to top-right
    flipped = np.flipud(matrix)
    for k in range(-flipped.shape[0], flipped.shape[1]):
        count += count_arr_matches(flipped.diagonal(offset=k))

    return count


def count_cross_mas_matches(matrix: np.ndarray) -> int:
    n_matches = 0

    starts = np.array(np.where(matrix == "A")).T

    for i in range(starts.shape[0]):
        index = starts[i]

        if index[0] == 0 or index[0] == matrix.shape[0] - 1 or index[1] == 0 or index[1] == matrix.shape[1] - 1:
            continue

        top_left, top_right, bottom_left, bottom_right = (str(matrix[tuple(index + np.array([-1, -1]))]),
                                                          str(matrix[tuple(index + np.array([1, -1]))]),
                                                          str(matrix[tuple(index + np.array([-1, 1]))]),
                                                          str(matrix[tuple(index + np.array([1, 1]))]))

        if (re.match("[MS]", top_left) and re.match("[MS]", bottom_right) and bottom_right != top_left and
                re.match("[MS]", top_right) and re.match("[MS]", bottom_left) and bottom_left != top_right):
            n_matches += 1


    return n_matches


if __name__ == "__main__":
    char_list = []
    with open("../data/data_day4.txt", "r") as f:
        for line in f:
            line_chars = []
            for char in line:
                if char != "\n":
                    line_chars.append(char)
            char_list.append(line_chars)

    char_arr = np.array(char_list)

    print(count_cross_mas_matches(char_arr))
