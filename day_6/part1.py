def main():
    with open('input.txt', 'r') as fh:
        counter = parse_signal(fh)
    print('counter',counter)

def parse_signal(fh):
    step_counter = 4
    char = fh.read(4)
    file_data = char
    while char:
        char = fh.read(1)
        #print('char', char, '\nfile data', file_data, '\ncounter', step_counter)
        #print('\n')
        if check_SOP(file_data):
            return step_counter
        file_data = file_data[1:]
        file_data += char
        step_counter += 1
    print('ended parsing')
    return False

def check_SOP(data):
    """
    ahora checkea en todo el string, entonces siempre encuentra una instancia 
    del char. Desarrollar forma en la cual busca en el resto del string;
    si se usan contadores tener en cuanta forma de handlear el error cuando el
    contador llegue al final del string "data"
    """
    count = 1
    for c in data:
        if count == 4:
            print('data in good check',data)
            return True
        if c in data[count:]:
            return False
        count += 1
    


main()
