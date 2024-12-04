import numpy as np
import re


def find_matches(arr):
    return len(re.findall("XMAS", "".join(arr))) + len(re.findall("SAMX", "".join(arr)))


def find_xmas_matches(matrix):
    count = 0

    # Rows
    for i in range(char_arr.shape[0]):
        count += find_matches(char_arr[i, :])

    # Cols
    for j in range(char_arr.shape[1]):
        count += find_matches(char_arr[:, j])

    # Diagonals top-left to bottom-right
    for k in range(-char_arr.shape[0], char_arr.shape[1]):
        count += find_matches(char_arr.diagonal(offset=k))

    # Diagonals bottom-left to top-right
    flipped = np.flipud(char_arr)
    for k in range(-flipped.shape[0], flipped.shape[1]):
        count += find_matches(flipped.diagonal(offset=k))

    return count


def find_cross_mas_matches(matrix):
    n_matches = 0

    starts = np.array(np.where(matrix == "A")).T

    for i in range(starts.shape[0]):
        index = starts[i]
        first = False

        # Begin ugly code
        if index[0] == 0 or index[0] == matrix.shape[0] - 1 or index[1] == 0 or index[1] == matrix.shape[1] - 1:
            continue

        # Check first diagonal
        match matrix[tuple(index + np.array([-1, -1]))]:
            case "M":
                if matrix[tuple(index + np.array([1, 1]))] == "S":
                    first = True
            case "S":
                if matrix[tuple(index + np.array([1, 1]))] == "M":
                    first = True

        # Check second diagonal
        if first:
            match matrix[tuple(index + np.array([-1, 1]))]:
                case "M":
                    if matrix[tuple(index + np.array([1, -1]))] == "S":
                        n_matches += 1
                case "S":
                    if matrix[tuple(index + np.array([1, -1]))] == "M":
                        n_matches += 1

        # End ugly code

    return n_matches


if __name__ == "__main__":
    char_matrix = []
    with open("data_day4.txt", "r") as f:
        for line in f:
            line_chars = []
            for char in line:
                if char != "\n":
                    line_chars.append(char)
            char_matrix.append(line_chars)

    char_arr = np.array(char_matrix)

    print(find_cross_mas_matches(char_arr))
