
def main():
    group_counter = priorities_sum = 0

    with open('input.txt', 'r') as fh:
        line = fh.readline().strip('\n')
        while line:
            if group_counter == 0:
                badges = get_items(line)
                group_counter += 1
            elif group_counter == 1:
                items = get_items(line)
                badges = compare_badges(badges, items)
                group_counter += 1
            elif group_counter == 2:
                items = get_items(line)
                badges = compare_badges(badges, items)
                priorities_sum += give_priority(badges[0])
                group_counter = 0

            line = fh.readline().strip('\n')
    print('total priorities', priorities_sum)


def get_items(rucksk):
    items = []
    for i in rucksk:
        items.append(i) if i not in items else None
    return items

def compare_badges(badges, items):
    new_badges = []
    for b in badges:
        new_badges.append(b) if b in items else None
    return new_badges

def give_priority(letter):
    code = ord(letter)
    if code >= 97:
        return code - 96
    elif code <= 90:
        return code - 38


main()
