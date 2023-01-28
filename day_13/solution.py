import json


def main():
    global log
    log = open('work_log.txt', 'w')
    with open('input.txt', 'r') as fh:
        ordered_indices = read_file(fh)
    log.close()
    # print('the sum of the packets indices is', sum(ordered_indices))
    # print(ordered_indices)
    return ordered_indices


def print_log(*msg):
    log.write(' '.join([str(i) for i in msg]))
    log.write('\n')


def read_file(fh):
    index = packet_count = 1
    ordered_indices = []
    ordered_pair = False
    for line in fh:
        if line == '\n':
            depth = 0
            print_log('-------------')
            print_log('checking packet', index)
            ordered_pair = check_packet_data(left_packet, right_packet, depth)
            if ordered_pair:
                print_log('ORDERED packet', index)
                ordered_indices.append(index)
            packet_count = 1
            index += 1
        elif packet_count == 1:
            left_packet = json_decode(line)
            packet_count += 1
        elif packet_count == 2:
            right_packet = json_decode(line)

    return ordered_indices


def json_decode(line):
    try:
        packet = json.loads(line.strip())
        return packet
    except json.decoder.JSONDecodeError as err:
        print('error', err.msg, 'in pos', err.pos)
        print('line', line.strip())


def check_packet_data(left, right, depth):
    # input()
    ordered = False
    # check types
    left_type, right_type = type(left), type(right)
    len_left = len(left) if left_type is list else 'int'
    len_right = len(right) if right_type is list else 'int'
    print_log()
    print_log('depth:', depth, 'len L:', len_left, 'len R:', len_right)
    print_log('L', left)
    print_log('R', right, '\n')
    if left_type is list and right_type is list:
        # print('both lists')
        ordered = compare_lists(left, right, depth)
    elif left_type is list:
        # print('left lists')
        ordered = compare_lists(left, [right], depth, True)
    elif right_type is list:
        # print('right lists')
        ordered = compare_lists([left], right, depth, True)
    else:
        # print('both int')
        ordered = compare_ints(left, right)
    print_log('ordered is:', ordered, 'depth is', depth) 

    return ordered


def compare_lists(left, right, depth, converted=False):
    ordered = None
    # if len(left) > len(right) and not converted:
        # print_log('left longer; len left', len(left), 'len right', len(right))
        # return False
    count = 0
    longest = max(len(left), len(right))
    if longest == 0:
        print_log('comparing empty lists; depth', depth)
        return None
    while count < longest:
        try:
            left_item = left[count]
        except IndexError:
            print_log('left index error; depth', depth)
            return True
        try:
            right_item = right[count]
        except IndexError:
            print_log('right index error; depth', depth)
            return False 
        ordered = check_packet_data(left_item, right_item, depth + 1)
        count += 1

        if converted and count == 1: return ordered
        if not ordered and ordered is not None: return False
        if ordered: return True


    return ordered


def compare_ints(left, right):
    print_log('left bigger'if left > right else 'right bigger')
    return left < right if left != right else None


main()

