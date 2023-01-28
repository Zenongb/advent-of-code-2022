
def main():
    crates = []
    with open('crates.txt', 'r') as fh:
        line = fh.readline().strip('\n')
        while line:
            crates.append([*line])
            line = fh.readline().strip('\n')
    print('starting crates', crates)
    with open('input.txt', 'r') as fh:
        line = fh.readline().strip('\n')
        while line:
            #parse moves
            moves = parse_moves(line)
            crates = move_crates(crates, moves)
            line = fh.readline().strip('\n')
    print('ending crates',crates)
    #make answer in one line
    ans = ''
    for l in crates:
        ans += l[-1]
    print('\nAnswer is',ans)
    return


def parse_moves(line):
    moves = []
    for a in line.split(' '):
        moves.append(int(a)) if a.isdigit() else None
    return moves

def move_crates(crates, moves):
    # moves [amt, from, to]
    amt, fr, to = moves
    fr, to = fr-1, to-1
    lenfr = len(crates[fr])
    to_move = crates[fr][-amt::]
    crates[fr] = crates[fr][:lenfr - amt]
    crates[to].extend(to_move)
    return crates


main()
