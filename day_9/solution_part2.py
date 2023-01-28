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
    tail_positions = ['0/0']
    rope = ['0/0' for _ in range(10)]
    for step in steps:
        rope, tail_moves = simulate_movement(step, rope)
        tail_positions.extend(tail_moves)
    print('the final rope is', rope)
    return tail_positions


def simulate_movement(step, rope):
    dir, amt = step.split()
    tail_moves = []
    # the plane grows to the right and upwards
    for _ in range(int(amt)):
        rope[0] = move(dir, rope[0])
        for k in range(1, len(rope)):
            rope[k] = move_knots(rope[k-1], rope[k])
        tail_moves.append(rope[-1])

    return rope, tail_moves


def move_knots(head_pos, tail_pos):
    head_x, head_y = parse_pos(head_pos)
    tail_x, tail_y = parse_pos(tail_pos)
    # calc distance
    dist_x = head_x - tail_x
    dist_y = head_y - tail_y

    # handle diag movement
    if abs(dist_x) == 2 and abs(dist_y) == 2:
        return pos_compose(head_x - dist_x // 2, head_y - dist_y // 2)
    elif abs(dist_x) == 2 and abs(dist_y) == 1:
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
