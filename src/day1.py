import numpy as np
import pandas as pd


if __name__=="__main__":
    df = pd.read_csv("../data/data_day1.csv")

    # Part 1
    sorted_1, sorted_2 = np.sort(df["list1"]), np.sort(df["list2"])
    summed = np.abs(sorted_1 - sorted_2)
    print(f"Total part 1: {np.sum(summed)}")

    # Part 2
    counts = np.vectorize(lambda ele: df["list2"][df["list2"]==ele].shape[0] * ele)(df["list1"])
    print(f"Total part 2: {np.sum(counts)}")
