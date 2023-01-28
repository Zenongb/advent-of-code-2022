"""
A rock
B paper
C scissors

X rock - 1 point
Y paper - 2 points
Z scissors - 3 points

lost =  0 points
draw = 3 points
win = 6 points
"""

def main():
    total_score = 0
    with open("input.txt", "r") as fh:
        line = fh.readline().strip('\n')
        while line:
            round_score = define_round(line) 
            print('round_score', round_score)
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
        return 1 + 3
    elif pl == "Y":
        return 2 + 6
    elif pl == "Z":
        return 3 + 0

def oponent_paper(pl):
    if pl == "X":
        return 1 + 0
    elif pl == "Y":
        return 2 + 3
    elif pl == "Z":
        return 3 + 6

def oponent_scissors(pl):
    if pl == "X":
        return 1 + 6
    elif pl == "Y":
        return 2 + 0
    elif pl == "Z":
        return 3 + 3



main()
