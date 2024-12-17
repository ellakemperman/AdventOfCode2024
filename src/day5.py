import numpy as np
import pandas as pd


def get_applicable_rules(ordering: list, rules: pd.DataFrame) -> np.ndarray:
    np_rules = rules.to_numpy()
    applicable_rules = np_rules[np.isin(np_rules[:, 0], ordering)]
    return applicable_rules[np.isin(applicable_rules[:, 1], ordering)]


def filter_ordering(ordering: list, rules: pd.DataFrame) -> bool:
    for rule in get_applicable_rules(ordering, rules):
        if ordering.index(rule[0]) > ordering.index(rule[1]):
            return False
    return True


def count_middle(orderings: list, rules: pd.DataFrame):
    filtered = filter(lambda ordering: filter_ordering(ordering, rules), orderings)
    return sum(map(lambda x: x[len(x) // 2], filtered))


def reorder_ordering(ordering: list[int], rules: pd.DataFrame):
    ordering = ordering.copy()
    i = 0
    reorders = 1
    applicable_rules = get_applicable_rules(ordering, rules)
    while i < applicable_rules.shape[0]:
        rule = applicable_rules[i]
        if (index0 := ordering.index(rule[0])) > (index1 := ordering.index(rule[1])):
            ordering[index0] = rule[1]
            ordering[index1] = rule[0]
            reorders += 1
            i = 0

        i += 1
    return ordering


def reorder_orderings(orderings: list, rules: pd.DataFrame) -> int:
    filtered = filter(lambda ordering: not filter_ordering(ordering, rules), orderings)
    reordered = map(lambda x : reorder_ordering(x, rules), filtered)
    return sum(map(lambda x: x[len(x) // 2], reordered))



if __name__ == "__main__":
    rules = pd.read_csv("../data/data_day5.csv")

    orderings = []
    with open("../data/data_day5.txt", "r") as f:
        for line in f:
            orderings.append(list(map(lambda x: int(x), line.strip("\n").split(","))))

    print(reorder_orderings(orderings, rules))
