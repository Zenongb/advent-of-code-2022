import numpy as np


def main():
    weighted_map = [l.strip() for l in open('input.txt', 'r')]
    print('len rows', len(weighted_map), 'len cols', len(weighted_map[0]))
    shortest_path = find_path(weighted_map)
    print(f'the shortest path uses {len(shortest_path)} steps')
    show_path(shortest_path, weighted_map)


def find_path(map):
    # A* pathfinding algo
    done = False
    start_coords, end_coords = start_and_end(map)
    start, end = node(np.array(start_coords), 'a'), node(np.array(end_coords), 'z')
    start['g_score'] = 0
    closed_list = []
    open_list = [start]
    while not done:
        selected_node = select_node(open_list)
        gather_frontier(selected_node, open_list, closed_list, map, end)
        # input('step')
        if find_by_coords(closed_list, end['coords']) > -1 or len(open_list) == 0:
            done = True
    return select_shortest_path(closed_list, start, end)


def select_shortest_path(closed_list, start, end):
    path = []
    tail_index = find_by_coords(closed_list, end['coords'])
    while True:
        tail_node = closed_list[tail_index]
        path.append(tail_node)
        if start['coords'].tolist() == tail_node['coords'].tolist():
            return path
        tail_index = find_by_coords(closed_list, tail_node['parent_coords'])


def start_and_end(map):
    row_count = 0
    for row in map:
        col_count = 0
        for col in row:
            if col == 'S':
                start = (row_count, col_count)
            elif col == 'E':
                end = (row_count, col_count)
            col_count += 1
        row_count += 1
    return start, end


def gather_frontier(current_node, open_list, closed_list, map, end):
    sides = [np.array((1, 0)),
             np.array((0, 1)),
             np.array((0, -1)),
             np.array((-1, 0))]
    for s in sides:
        open_coord = current_node['coords'] + s
        # check that the coord is inside the map
        if open_coord[0] < 0 or open_coord[0] >= len(map):
            # print('first coord bigger/lower', open_coord)
            continue
        elif open_coord[1] < 0 or open_coord[1] >= len(map[0]):
            # print('second coord bigger/lower', open_coord)
            continue
        # print('checking', open_coord)

        open_node = node(open_coord, get_elevation(map, open_coord))
        # check if you can traverse to the node because height
        if not traversable(current_node, open_node, 1):
            continue
        # check if the node exists in the closed array
        if find_by_coords(closed_list, open_node['coords']) >= 0:
            continue

        open_index = find_by_coords(open_list, open_node['coords'])

        if open_index >= 0:
            open_node = open_list[open_index]
            # calc G score
            if open_node['g_score'] > current_node['g_score'] + 10:
                open_node['g_score'] = current_node['g_score'] + 10
                open_node['parent_coords'] = current_node['coords']
        else:
            # calc G score
            open_node['g_score'] = current_node['g_score'] + 10
            open_node['parent_coords'] = current_node['coords']
            # calc H score
            open_node['h_score'] = calc_H_score(open_node, end)

            open_list.append(open_node)

    open_list.pop(find_by_coords(open_list, current_node['coords']))
    closed_list.append(current_node)


def select_node(open_list):
    # get some node to be the selected
    cheapest_node = open_list[-1]
    if len(open_list) == 1:
        return cheapest_node
    for node in open_list:
        if calc_f_cost(node) < calc_f_cost(cheapest_node):
            cheapest_node = node
    return cheapest_node


def calc_f_cost(node):
    return node['h_score'] + node['g_score']


def node(coords, elevation):
    # create a node instance
    # it also will have
    #   parent
    #   g_score
    #   h_score
    return {
        'coords': coords,
        'elevation': elevation,
        }


def calc_H_score(current, end):
    # Manhattan heuristic calculation
    distance_vector = end['coords'] - current['coords']
    return distance_vector[0] * 5 + distance_vector[1] * 5


def get_elevation(map, coords):
    # check the map and grab the elevation
    elevation = map[coords[0]][coords[1]]
    return 'z' if elevation == 'E' else elevation


def traversable(_from, to, elevation):
    # check if you can walk from one node to the other
    if ord(_from['elevation']) >= ord(to['elevation']) - elevation:
        # if ord(_from['elevation']) <= ord(to['elevation']) + elevation:
        return True
    return False


def find_by_coords(array, coords):
    # search in list to find if the object with the given coords exists and
    # return the index, if not in the list return -1
    index = 0
    for node in array:
        if node['coords'].tolist() == coords.tolist():
            return index
        index += 1
    return -1


def show_path(path, map):
    last = len(path) - 2
    map = [[*l] for l in map]
    for node in path[::-1]:
        c = node['coords']
        if last >= 0:
            char = move(c, path[last]['coords'])
        else:
            char = '0'
        map[c[0]][c[1]] = char
        last -= 1
    new_map = []
    for r in map:
        new_map.append(''.join(r))
    for l in new_map:
        print(l)


def move(curr, last):
    data = curr - last
    if [1, 0] == data.tolist():
        return '^'
    elif [-1, 0] == data.tolist():
        return 'v'
    elif [0, 1] == data.tolist():
        return '<'
    elif [0, -1] == data.tolist():
        return '>'
    return 'E'


main()
