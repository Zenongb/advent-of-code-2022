"""
A rock
B paper
C scissors

X lose - 0 point
Y draw - 3 points
Z win - 6 points

"""

def main():
    total_score = 0
    with open("input.txt", "r") as fh:
        line = fh.readline().strip('\n')
        while line:
            round_score = define_round(line) 
            total_score += round_score
            line = fh.readline().strip('\n')
    print("total score", total_score)


def define_round(line):
    total = 0
    [op, pl] = line.split(' ')
    op, pl = op.strip(' '), pl.strip(' ')
    if op == "A":
        total += oponent_rock(pl)
    elif op == "B":
        total += oponent_paper(pl)
    elif op == "C":
        total += oponent_scissors(pl)
    return total

def oponent_rock(pl):
    if pl == "X":
        return 0 + 3
    elif pl == "Y":
        return 3 + 1
    elif pl == "Z":
        return 6 + 2


def oponent_paper(pl):
    if pl == "X":
        return 0 + 1
    elif pl == "Y":
        return 3 + 2
    elif pl == "Z":
        return 6 + 3


def oponent_scissors(pl):
    if pl == "X":
        return 0 + 2
    elif pl == "Y":
        return 3 + 3
    elif pl == "Z":
        return 6 + 1


main()
