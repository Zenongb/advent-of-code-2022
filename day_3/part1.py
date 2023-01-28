
def main():
    priorities_sum = 0
    with open('input.txt', 'r') as fh:
        line = fh.readline().strip('\n')
        while line:
            priorities_sum += parse_rucksack(line)
            line = fh.readline().strip('\n')
    print('total priorities', priorities_sum)

def parse_rucksack(rucksk):
    divider = len(rucksk) // 2
    items = get_items(rucksk[:divider])
    repeated_item = ''
    for i in rucksk[divider:]:
        if i in items:
            repeated_item = i
            break
    return give_priority(repeated_item)

def get_items(compartment):
    items = []
    for i in compartment:
        items.append(i) if i not in items else None
    return items

def give_priority(letter):
    code = ord(letter)
    if code >= 97:
        return code - 96
    elif code <= 90:
        return code - 38

main()
