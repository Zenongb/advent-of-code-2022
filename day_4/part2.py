
def main():
    overlaping_ranges = 0
    with open("input.txt", "r") as fh:
       line = fh.readline() 
       while line:
           assign_pairs = parse_line(line)
           print('assigns',assign_pairs)
           overlaping_ranges += check_overlap(assign_pairs)
           line = fh.readline() 
    print('overlapping_ranges', overlaping_ranges)


def parse_line(line):
    parsed_assignments = []
    line = line.strip('\n')
    for a in line.split(','):
        assignment = a.split('-')
        parsed_assignments.append([int(assignment[0]), int(assignment[1])])
    return parsed_assignments

def check_overlap(assign_pairs):
    a0 = assign_pairs[0]
    a1 = assign_pairs[1]
    if a0[0] <= a1[0] and a0[1] >= a1[1]:
        return 1
    elif a0[0] >= a1[0] and a0[1] <= a1[1]:
        return 1
    elif a0[0] <= a1[0] and a0[1] >= a1[0]:
        return 1
    elif a1[0] <= a0[0] and a1[1] >= a0[0]:
        return 1
    return 0


main()
