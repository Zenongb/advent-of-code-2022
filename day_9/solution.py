def main():
    with open('input.txt', 'r') as fh:
        steps = fh.readlines()
    steps = [line.strip() for line in steps]

    tail_pos = parse_steps(steps)
    unique_pos = []
    for pos in tail_pos:
        if pos not in unique_pos:
            unique_pos.append(pos)
    print('the amount of positions where the tail stepped at least once is', len(unique_pos))


def parse_steps(steps):
    head_positions = ['0/0']
    tail_positions = ['0/0']
    for step in steps:
        head, tail = simulate_movement(step, head_positions[-1], tail_positions[-1])
        head_positions.extend(head)
        tail_positions.extend(tail)
    return tail_positions


def simulate_movement(step, head_init_pos, tail_init_pos):
    dir, amt = step.split()
    head_moves = [head_init_pos]
    tail_moves = [tail_init_pos]
    # the plane grows to the right and upwards
    for c in range(int(amt)):
        head_moves.append(move(dir, head_moves[-1]))
        new_tail_pos = move_tail(head_moves[-1], tail_moves[-1])
        tail_moves.append(new_tail_pos)

    head_moves.pop(0)
    tail_moves.pop(0)
    return head_moves, tail_moves


def move_tail(head_pos, tail_pos):
    head_x, head_y = parse_pos(head_pos)
    tail_x, tail_y = parse_pos(tail_pos)
    # calc distance
    dist_x = head_x - tail_x
    dist_y = head_y - tail_y

    # handle diag movement
    if abs(dist_x) == 2 and abs(dist_y) == 1:
        return pos_compose(head_x - dist_x // 2, head_y)
    elif abs(dist_y) == 2 and abs(dist_x) == 1:
        return pos_compose(head_x, head_y - dist_y // 2)
    # handle linear movement
    elif abs(dist_x) == 2:
        return pos_compose(head_x - dist_x // 2, head_y)
    elif abs(dist_y) == 2:
        return pos_compose(head_x, head_y - dist_y // 2)

    return tail_pos


def move(dir, pos):
    x, y = parse_pos(pos)
    if dir == 'U':
        return pos_compose(x, y + 1)
    elif dir == 'R':
        return pos_compose(x + 1, y)
    elif dir == 'D':
        return pos_compose(x, y - 1)
    elif dir == 'L':
        return pos_compose(x - 1, y)


def parse_pos(position):
    x, y = position.split('/')
    return int(x), int(y)


def pos_compose(x, y):
    return f'{x}/{y}'


main()
