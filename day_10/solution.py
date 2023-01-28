

def main():

    commands = [line.strip() for line in open('input.txt', 'r')]
    screen = simulate_commands(commands)
    for _ in range(8):
        print(screen[:40])
        screen = screen[40:]
    pass


def simulate_commands(commands):
    cycle = 0
    registry = 1
    screen = ''
    for comm in commands:
        if comm == 'noop':
            cycle, screen = update_cycles(1, registry, cycle, screen)
        elif comm[:4] == 'addx':
            [_, amt] = comm.split()
            cycle, screen = update_cycles(2, registry, cycle, screen)
            registry += int(amt)

    return screen


def update_cycles(amt, registry, cycle,  screen):
    for _ in range(amt):
        screen += output_pixel(cycle, registry)
        cycle += 1
        if cycle == 40:
            cycle = 0

    return cycle, screen


def output_pixel(cycle, registry):
    if registry + 1 >= cycle and registry - 1 <= cycle:
        return '#'
    return ' '


main()
