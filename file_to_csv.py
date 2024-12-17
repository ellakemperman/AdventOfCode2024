import re


if __name__ == "__main__":
    f_name = "test.csv"
    pattern = "[A-Z]"

    with open(f_name, "r") as f:
        lines = f.readlines()

    with open(f_name, "w") as f:
        for line in lines:
            f.write(re.sub(pattern, "\g<0>,", line)[:-1])
            f.write("\n")

