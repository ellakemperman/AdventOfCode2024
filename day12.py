import numpy as np
import pandas as pd

def calc_area_perimeter(data: np.ndarray, plant: str) -> int:
    directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
    found = set()
    all_coords = np.array(np.where(data == plant)).T
    total = 0

    def inner(coordinates: np.ndarray) -> tuple[int, int]:
        # Recursive case
        found.add(tuple(coordinates))
        perimeter = 0
        area = 1
        for direction in directions:
            check_coords = coordinates + direction
            if (np.zeros(2) <= check_coords).all() and (check_coords < data.shape).all() and data[tuple(check_coords)] == plant:
                if tuple(check_coords) not in found:
                    add_perimeter, add_area = inner(check_coords)
                    perimeter += add_perimeter
                    area += add_area
            else:
                # print(check_coords)
                perimeter += 1

        return perimeter, area

    while all_coords.size > 0:
        perimeter, area = inner(all_coords[0])
        total += area * perimeter
        for coords in found:
            all_coords = all_coords[np.logical_not(np.equal(all_coords, coords).all(axis=1))]
        found.clear()

    return total


def calc_all_area_perimeter(data: np.ndarray) -> int:
    plants = np.unique(data)
    total = 0
    for plant in plants:
        total += calc_area_perimeter(data, plant)
    return total


if __name__ == "__main__":
    data = pd.read_csv("data_day12.csv", header=None).to_numpy()
    print(calc_all_area_perimeter(data))
