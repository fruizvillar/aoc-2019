from lib import read_stdin
import pandas as pd

TEST = False

DESIRED_OUT = 19690720

class HaltException(Exception):
    pass


def call_func(array, pos):
    func = FUNCTIONS[array[pos]]
    return func(array, pos)


def suma(array, pos):
    if array[pos] != 1:
        raise RuntimeError('SUM is 1')
    print('Summing {} with {} and storing in {}'.format(array[pos + 1], array[pos + 2], array[pos + 3]))
    array[array[pos + 3]] = array[array[pos + 2]] + array[array[pos + 1]]
    return array


def multiply(array, pos):
    if array[pos] != 2:
        raise RuntimeError('MUL is 2')
    print('Multiplying {} with {} and storing in {}'.format(array[pos + 1], array[pos + 2], array[pos + 3]))
    array[array[pos + 3]] = array[array[pos + 2]] * array[array[pos + 1]]

    return array


def halt(array, pos):
    if array[pos] != 99:
        raise RuntimeError('HALT is 99')

    raise HaltException


FUNCTIONS = {1: suma, 2: multiply, 99: halt}


def run_program(array):
    print(array)
    try:
        for i in [r * 4 for r in range(len(array) // 4)]:
            print(i, array[i:i + 4])
            array = call_func(array, i)
            print(array)

    except HaltException:
        print('Halted')
    return array


def main():
    i = 0
    for noun in range(99):
        for verb in range(99):
            i += 1
            array = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 10, 19, 1, 9, 19, 23, 1, 13, 23, 27, 1, 5, 27, 31, 2,
                     31, 6, 35, 1, 35, 5, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 5, 51, 2, 10, 51, 55, 1, 5, 55, 59, 1, 59, 5,
                     63, 2, 63, 9, 67, 1, 67, 5, 71, 2, 9, 71, 75, 1, 75, 5, 79, 1, 10, 79, 83, 1, 83, 10, 87, 1, 10, 87, 91, 1,
                     6, 91, 95, 2, 95, 6, 99, 2, 99, 9, 103, 1, 103, 6, 107, 1, 13, 107, 111, 1, 13, 111, 115, 2, 115, 9, 119,
                     1, 119, 6, 123, 2, 9, 123, 127, 1, 127, 5, 131, 1, 131, 5, 135, 1, 135, 5, 139, 2, 10, 139, 143, 2, 143,
                     10, 147, 1, 147, 5, 151, 1, 151, 2, 155, 1, 155, 13, 0, 99, 2, 14, 0, 0]
            array[1] = noun
            array[2] = verb
            array = run_program(array)
            result = array[0]
            print('Noun {}, verb {}, result={}. (value={})'.format(noun, verb, result, noun*100 + verb))
            if result == DESIRED_OUT:
                print('Done in exec {}'.format(i))
                exit(0)


def test():
    array = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    array = run_program(array)
    print(array)


if __name__ == '__main__':
    if TEST:
        test()
    else:
        main()
