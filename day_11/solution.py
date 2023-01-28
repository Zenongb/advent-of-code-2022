import math


def main():
    with open('input.txt', 'r') as fh:
        lines = [line.strip() for line in fh.readlines()]
    monkeys = parse_monkeys(lines)
    print(monkeys)
    monkey_passes = play_rounds(monkeys, 10000)
    print('the total passes for the monkos are:')
    print(monkey_passes)
    first_biggest = second_biggest = 0
    for k, v in monkey_passes.items():
        if v > first_biggest:
            second_biggest = first_biggest
            first_biggest = v
        elif v > second_biggest:
            second_biggest = v
        print(f'monkey {k} touched {v} items')

    print("the two biggest values are: ", first_biggest, second_biggest)
    print('tha nas to the part one is', first_biggest * second_biggest)
    pass


def parse_monkeys(lines):
    monkeys = {}
    count = 0
    in_monkey = None
    while count < len(lines):
        if lines[count][:6] == 'Monkey':
            [_, num] = lines[count].split()
            in_monkey = int(num[0])
            monkeys[in_monkey] = {}
        elif lines[count][:15] == 'Starting items:':
            datum = lines[count][15:].split()
            monkeys[in_monkey]['robbed_items'] = [int(d.strip(',')) for d in datum]
        elif lines[count][:10] == 'Operation:':
            monkeys[in_monkey]['operation'] = lines[count][17:]
        elif lines[count][:5] == 'Test:':
            monkeys[in_monkey]['div_by'] = int(lines[count][19:])
        elif lines[count][:7] == 'If true':
            monkeys[in_monkey]['true'] = int(lines[count][-1])
        elif lines[count][:8] == 'If false':
            monkeys[in_monkey]['false'] = int(lines[count][-1])
        count += 1
    return monkeys


def play_rounds(monkeys, rounds):
    sm = [m['div_by'] for m in monkeys.values()]
    super_modulo = math.prod(sm)
    passes = {n: 0 for n in range(len(monkeys))}
    for r in range(rounds):
        playing = 0
        print('round', r)
        while playing < len(monkeys.keys()):
            monkey_turn(super_modulo, monkeys, passes, playing)
            playing += 1
    print(monkeys)
    return passes


def monkey_turn(super_modulo, monkeys, passes, playing):
    m = monkeys[playing]
    print(f'monko {playing} items {m["robbed_items"]}')
    for item in m['robbed_items']:
        # inspect
        passes[playing] += 1
        item = eval(m['operation'], {'old': item})
        # get bored
        # item = item // 3
        item = item % super_modulo
        # pass
        if item % m['div_by'] == 0:
            monkeys[m['true']]['robbed_items'].append(item)
        else:
            monkeys[m['false']]['robbed_items'].append(item)
    m['robbed_items'] = []


main()
