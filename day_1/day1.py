
def main():
    sum = max = max_1 = max_2 = 0
    with open("day1_input.txt") as fh:
        line = fh.readline()
        while line:
            if line == "\n":
                if sum > max:
                    max, max_1, max_2 = sum, max, max_1
                    print('max', max, max_1, max_2)
                elif sum > max_1:
                    max_1, max_2 = sum, max_1
                    print('max_1', max, max_1, max_2)
                elif sum > max_2:
                    max_2 = sum
                    print('max_2', max, max_1, max_2)
                sum = 0
            else:
                num = int(line.strip('\n'))
                sum += num
            line = fh.readline()
    print('maxes', max, max_1, max_2)
    return max + max_1 + max_2
                
final_max = main()
print(final_max)

