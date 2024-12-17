import numpy as np
import time




class Antenna:

    def __init__(self, char: str, coords: np.array):
        self.char = char
        self.coordinates = coords

    def __eq__(self, other):
        if isinstance(other, Antenna):
            return self.char == other.char and (self.coordinates == other.coordinates).all()
        return False

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return self.char + " @ " + str(self.coordinates)

    def __repr__(self):
        return str(self)


def get_matches(char, antennas):
    return list(filter(lambda x: x.char == char, antennas))


def compute_antinodes(antenna1: Antenna, antenna2: Antenna, n_harmonics: int) -> list:
    coords1, coords2 = antenna1.coordinates, antenna2.coordinates
    distance_vector = coords2 - coords1
    returns = []
    start = 0
    if n_harmonics == 1:
        start = 1
    for i in range(start, n_harmonics + 1):
        returns.append(tuple(coords1 - i * distance_vector))
        returns.append(tuple(coords2 + i * distance_vector))
    return returns


def compute_all_antinodes(antennas: list[Antenna], map_size: np.array, n_harmonics=1) -> int:
    antinodes = set()
    antennas_copy = antennas.copy()
    while len(antennas_copy) != 0:
        matches = get_matches(antennas_copy[0].char, antennas_copy)

        for match in matches.copy():
            matches.remove(match)
            antennas_copy.remove(match)
            for other in matches:
                nodes = compute_antinodes(match, other, n_harmonics)
                for antinode in nodes:
                    antinodes.add(antinode)

    return len(tuple(filter(lambda x: (np.array([-1, -1]) < np.array(x)).all() and (np.array(x) < map_size).all(), antinodes)))


if __name__ == "__main__":
    antennas = []

    with open("../data/data_day8.txt", "r") as f:
        for i, line in enumerate(f):
            for j, char in enumerate(line):
                if char != ".":
                    antennas.append(Antenna(char, np.array([i, j])))
    shape = np.array([i + 1, j + 1])
    start_time = time.time()
    print(compute_all_antinodes(antennas, shape, n_harmonics=50))
    print(time.time() - start_time)