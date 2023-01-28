import numpy as np


def main():
    weighted_map = [l.strip() for l in open('input.txt', 'r')]
    print('len rows', len(weighted_map), 'len cols', len(weighted_map[0]))
    start_coords, end_coords = start_and_end(weighted_map)
    starting_coords = gather_starting_coords(weighted_map)
    starting_coords.append(start_coords)
    path_lens = []
    shortest_path = []
    for a_coord in starting_coords:
        shortest_path, destination_confirmed = find_path(a_coord, end_coords, shortest_path, weighted_map)
        if destination_confirmed:
            print(f'from {a_coord} to {end_coords}')
            print(f'this path uses {len(shortest_path) - 1} steps')
            # show_path(shortest_path, weighted_map)
            path_lens.append((len(shortest_path), shortest_path))

    # find the shortest
    shortest = sorted(path_lens, key=lambda x: x[0])[0]
    print(f'the shortest path is {shortest[0] - 1} steps, and starts from')
    # show_path(shortest[1], weighted_map)


def gather_starting_coords(map):
    a_coords = []
    row_count = 0
    for row in map:
        col_count = 0
        for char in row:
            if char == 'a':
                a_coords.append((row_count, col_count))
            col_count += 1
        row_count += 1
    print('the amount of "a" elevantions in the map is', len(a_coords))
    return a_coords


def find_path(start_coords, end_coords, last_path, map):
    # A* pathfinding algo
    done = False
    start, end = node(np.array(start_coords), 'a'), node(np.array(end_coords), 'z')
    start['g_score'] = 0
    closed_list = []
    open_list = [start]
    pathing_checks = False
    destination_confirmed = True
    while not done:
        selected_node = select_node(open_list)
        gather_frontier(selected_node, open_list, closed_list, map, end)
        # compare paths to check if the search became redundant
        pathing_checks = compare_paths(grab_path(closed_list), last_path)
        # input('step')
        if find_by_coords(closed_list, end['coords']) > -1 or len(open_list) == 0:
            if len(open_list) == 0:
                return last_path, False
            done = True
        if pathing_checks:
            print('saved time with comparator')
            index = find_by_coords(last_path, closed_list[-1]['coords'])
            closed_list.extend(last_path[index::-1])
            done = True
    return select_shortest_path(closed_list, start, end), destination_confirmed


def compare_paths(nodes, path):
    # change
    if len(nodes) == 0:
        return False
    overlapping_index = find_by_coords(path, nodes[0]['coords'])
    if overlapping_index < 0:
        return False
    for node in nodes:
        if not node['coords'].tolist() == path[overlapping_index]['coords'].tolist():
            return False
        if overlapping_index == 0:
            break
        overlapping_index -= 1
    return True


def grab_path(closed_list):
    last_path = [closed_list[-1]]
    for _ in range(5):
        try:
            parent = last_path[-1]['parent_coords']
        except:
            return last_path
        parent_index = find_by_coords(closed_list, parent)
        if parent_index == -1:
            return last_path
        last_path.append(closed_list[parent_index])
    return last_path


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
    return abs(distance_vector[0] * 5) + abs(distance_vector[1] * 5)


def get_elevation(map, coords):
    # check the map and grab the elevation
    elevation = map[coords[0]][coords[1]]
    if elevation == 'E':
        elevation = 'z'
    elif elevation == 'S':
        elevation = 'a'
    return elevation


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
