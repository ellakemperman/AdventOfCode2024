def check_pattern(desired: str, available: set[str]) -> bool:
    evaluated = set()
    def inner(desired: str) -> bool:
        if desired in evaluated:
            return False

        evaluated.add(desired)
        # Base Case
        if len(desired) == 0:
            return True

        for match_pointer in range(1, len(desired) + 1):
            match_str = desired[0:match_pointer]
            if match_str in available and inner(desired[match_pointer:]):
                return True

        return False

    return inner(desired)

"""
def find_all_combinations(desire: str, available: set[str]) -> int:
    min_split_size = min([len(towel) for towel in available])
    def inner(desire: str, depth=0) -> int:
        total = 0
        for split_index in range(min_split_size, len(desire) - min_split_size):
            split1, split2 = desire[0:split_index], desire[split_index:]
            if check_pattern(split1, available) and check_pattern(split2, available):
                first, second = inner(split1, depth + 1), inner(split2, depth + 1)
                print(split1, split2)
                print(first, second)
                total += first * second
        if total == 0:
            total = 1
        return total
    x = inner(desire)
    print(x)
    return x
"""

def find_all_possible_desired(desires: list[str], available: set[str]) -> int:
    return len(tuple(filter(lambda desired: check_pattern(desired, available), desires)))


def sum_all_alternatives(desires: list[str], available: set[str]) -> int:
    filtered = tuple(filter(lambda desired: check_pattern(desired, available), desires))
    return sum(tuple(map(lambda desired: find_all_combinations(desired, available), filtered[1:2])))


# Find all possible splits causing both sides of the array to be valid. Then recurse until no valid splits, compute all
# valid position assignment and multiply at next level. Sum all results of splits at each level.


if __name__ == "__main__":
    with open("../data/test.csv", "r") as f:
        desires = []
        available = set(f.readline()[0:-1].split(","))
        f.readline()
        for line in f.readlines():
            desires.append(line[0:-1])

    # print(find_all_possible_desired(desires, available))
    print(sum_all_alternatives(desires, available))