def check_pattern(desired: str, available: set[str]) -> int:
    evaluated = dict()
    def inner(desired: str) -> int:
        try:
            return evaluated[desired]
        except KeyError:
            pass

        # Base Case
        if len(desired) == 0:
            return 1

        total = 0
        for match_pointer in range(1, len(desired) + 1):
            match_str = desired[0:match_pointer]
            if match_str in available:
                total += inner(desired[match_pointer:])

        evaluated[desired] = total
        return total

    return inner(desired)


def find_all_possible_desired(desires: list[str], available: set[str]) -> int:
    return len(tuple(filter(lambda desired: check_pattern(desired, available), desires)))


def sum_all_alternatives(desires: list[str], available: set[str]) -> int:
    return sum(tuple(map(lambda desired: check_pattern(desired, available), desires)))


if __name__ == "__main__":
    with open("../data/data_day19.txt", "r") as f:
        desires = []
        available = set(f.readline()[0:-1].split(","))
        f.readline()
        for line in f.readlines():
            desires.append(line[0:-1])

    # print(find_all_possible_desired(desires, available))
    print(sum_all_alternatives(desires, available))