import math


def main():
    with open('input.txt', 'r') as fh:
        map = fh.readlines()
    map = [m.strip() for m in map]
    exposed_coords = check_map(map)
    print('the number of exposed trees is', len(exposed_coords))
    scenic_scores = map_scenic_scores(map)
    print('the highest scenic view is', max(scenic_scores))


def check_map(map):
    exposed_trees = []  # arr of str with form '{row}{col}'
    # horizontal check
    row_count = 0
    for row in map:

        if row_count == 0 or row_count == len(map) - 1:
            exposed_trees.extend(f'{row_count}/{c}' for c in range(len(map[0])))
            row_count += 1
            continue

        # from left to right
        highest = col_count = 0
        for c in row:
            c = int(c)
            if c > highest:
                exposed_trees = add_tree(exposed_trees, row_count, col_count)
                highest = c
            col_count += 1

        # form right to left
        highest, col_count = 0, len(row) - 1
        for c in row[::-1]:
            c = int(c)
            if c > highest:
                exposed_trees = add_tree(exposed_trees, row_count, col_count)
                highest = c
            col_count -= 1

        row_count += 1

    # vertical check
    col_count = 0
    while col_count < len(map[0]):

        if col_count == 0 or col_count == len(map[0]) - 1:
            for r in range(len(map)):
                exposed_trees = add_tree(exposed_trees, r, col_count)
            col_count += 1
            continue

        # from top to bot
        highest = row_count = 0
        for row in map:
            height = int(row[col_count])
            if height > highest:
                exposed_trees = add_tree(exposed_trees, row_count, col_count)
                highest = height
            row_count += 1

        # from bot to top
        highest, row_count = 0, len(map) - 1
        for row in map[::-1]:
            height = int(row[col_count])
            if height > highest:
                exposed_trees = add_tree(exposed_trees, row_count, col_count)
                highest = height
            row_count -= 1

        col_count += 1

    return exposed_trees


def add_tree(exposed_trees, r, c):
    coord = f'{r}/{c}'
    if coord not in exposed_trees:
        exposed_trees.append(coord)
    return exposed_trees


def map_scenic_scores(map):
    scenic_scores = []
    row_count = 0
    for row in map:
        col_count = 0
        for col in row:
            coord = f'{row_count}/{col_count}'
            scenic_scores.append(calc_score(map, coord))
            col_count += 1
        row_count += 1
    return scenic_scores


def calc_score(map, coord):
    [row, col] = coord.split('/')
    row, col = int(row), int(col)
    tree_height = int(map[row][col])
    tc = [0, 0, 0, 0]  # total count

    print('checking coord', coord)
    # check sides
    left_done = right_done = up_done = down_done = False
    left_check, right_check = col - 1, col + 1
    up_check, down_check = row - 1, row + 1
    while True:
        # left
        if left_check >= 0 and not left_done:
            left_done, tc[0] = side_check(tc[0], tree_height, int(map[row][left_check]))
            left_check -= 1
        else:
            left_done = True

        # right
        if right_check < len(map[0]) and not right_done:
            right_done, tc[1] = side_check(tc[1], tree_height, int(map[row][right_check]))
            right_check += 1
        else:
            right_done = True

        # up
        if up_check >= 0 and not up_done:
            up_done, tc[2] = side_check(tc[2], tree_height, int(map[up_check][col]))
            up_check -= 1
        else:
            up_done = True

        # down
        if down_check < len(map) and not down_done:
            down_done, tc[3] = side_check(tc[3], tree_height, int(map[down_check][col]))
            down_check += 1
        else:
            down_done = True

        # end this
        if left_done and right_done and up_done and down_done:
            break

    print('total count', tc, math.prod(tc))
    return math.prod(tc)


def side_check(count, current_tree, comp_tree):
    done = False
    if current_tree > comp_tree:
        count += 1
    else:
        count += 1
        done = True
    return done, count


main()
