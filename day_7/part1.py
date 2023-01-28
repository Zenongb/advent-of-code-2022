

def main():
    with open('input.txt', 'r') as fh:
        file_system = build_fs(fh)
    check_sizes(file_system)

def build_fs(fh):
    file_sys = {}
    dir_hist = []
    line = fh.readline().strip('\n')
    while line:
        if line[0] == '$':
           file_sys, dir_hist = handle_command(file_sys, dir_hist, line) 
        else:
            file_sys = handle_ls(file_sys, dir_hist, line)

        line = fh.readline().strip('\n')
    return file_sys


def handle_command(file_sys, dir_hist, line):
    order = line.split()
    order.pop(0)
    if order[0] == 'cd':
        if order[1].isalpha():
            dir_hist.append(order[1])
        elif order[1] == '..':
            dir_hist.pop(-1)

    return file_sys, dir_hist

def handle_ls(file_sys, dir_hist, line):
    #if dir = {} if archive = size
    current_dir = file_sys
    data = line.split()
    for dir in dir_hist:
        current_dir = current_dir[dir]
    if data[0] == 'dir':
        current_dir[data[1]] = {}
    else:
        current_dir[data[1]] = int(data[0])
    return file_sys


def check_sizes(file_sys):
    print('in check sizes')
    home_dir_size, dir_sizes = handle_dir(file_sys)
    print('dir_sizes', dir_sizes)
    print('home_dir_sizes', home_dir_size)
    total_sum = sum_sizes(dir_sizes)
    print('total sum', total_sum)
    check_to_delete(dir_sizes)
    

def handle_dir(dir):
    current_dir_size = 0
    dir_sizes = {}
    for k,v in dir.items():
        if type(v) is dict:
            inner_dir_size, inner_dir_sizes = handle_dir(v)
            current_dir_size += inner_dir_size
            dir_sizes[k] = inner_dir_sizes
        elif type(v) is int:
            current_dir_size += v
    dir_sizes['total'] = current_dir_size
    return current_dir_size, dir_sizes

def sum_sizes(dir_sizes): #part1
    sum = dir_sizes['total'] if dir_sizes['total'] < 100000 else 0
    for v in dir_sizes.values():
        if type(v) is dict:
            sum += sum_sizes(v)
    return sum

def check_to_delete(dir_sizes):
    needed_size = 30000000 - (70000000 - dir_sizes['total'])
    size = check_closest(needed_size, dir_sizes['total'], dir_sizes)
    print('the size of the dir to delete is', size)

def check_closest(needed_size, cap, dir):
    cap = dir['total'] if dir['total'] > needed_size and dir['total'] < cap else cap
    for v in dir.values():
        if type(v) is dict and dir['total'] > needed_size:
            cap = check_closest(needed_size, cap, v)
    return cap

main()
