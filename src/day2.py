import numpy as np
import pandas as pd


def check_list(xs, removed=False):
    current = xs[0]
    for i, ele in enumerate(xs[1:]):
        if current < ele and ele - current <= 3:
            current = ele
            continue
        if not removed:
            return check_list(xs[0:i+1] + xs[i+2:], removed=True) or check_list(xs[0:i] + xs[i+1:], removed=True)
        return False
    return True


if __name__=="__main__":
    truths = []
    with open("../data/data_day2.csv", "r") as f:
        for line in f:
            xs = line.split(",")
            for i, item in enumerate(xs):
                xs[i] = int(item)

            reversed = xs.copy()
            reversed.reverse()

            truths.append(check_list(xs) or check_list(reversed))

    print(truths.count(True))


