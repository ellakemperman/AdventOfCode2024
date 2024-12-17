import pandas as pd
import numpy as np


def score_trailhead(data: np.ndarray, trailhead: np.array, allow_duplicate_ends: bool, max_value=9) -> int:
    directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
    found = set()

    def inner(value: int, coordinates: np.ndarray) -> int:
        # Base case
        if value == max_value and (allow_duplicate_ends or tuple(coordinates) not in found):
            found.add(tuple(coordinates))
            return 1

        # Recursive case
        score = 0
        for direction in directions:
            check_coords = coordinates + direction
            if (np.zeros(2) <= check_coords).all() and (check_coords < data.shape).all() and data[tuple(check_coords)] == value + 1:
                score += inner(value + 1, check_coords)
        return score

    return inner(0, trailhead)


def score_all_trailheads(data: np.ndarray, allow_duplicate_ends=False):
    trailheads = np.array(np.where(data == 0)).T
    return sum(map(lambda trailhead: score_trailhead(data, trailhead, allow_duplicate_ends), trailheads))


if __name__ == "__main__":
    data = pd.read_csv("data_day10.csv", header=None).to_numpy()

    # Allow duplicates is False for the first part of the assignment, True for the second.
    print(score_all_trailheads(data, allow_duplicate_ends=True))
