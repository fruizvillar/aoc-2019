TEST = True


class Coord:
    def __init__(self, x, y, n=0):
        self.x = x
        self.y = y
        self.d = abs(x) + abs(y)
        self.n = n

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y, self.n + 1)

    def __repr__(self):
        return f'({self.x}, {self.y})[{self.d}]{{{self.n}}}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x.__hash__() * self.y.__hash__()

    def __lt__(self, other):
        return self.n < other.n


DIR_V = {'R': Coord(1, 0), 'L': Coord(-1, 0), 'U': Coord(0, 1), 'D': Coord(0, -1)}


def get_coords(path):
    last_segment = Coord(0, 0)
    coords = {last_segment: 0}
    for segment in path.split(','):
        print(segment)
        direction = DIR_V[segment[0]]
        length = int(segment[1:])
        for step in range(1, length + 1):
            step_coord = last_segment + direction
            coords[step_coord] = 0
            print(step_coord, end=', ')
            last_segment = step_coord
        print()
    return coords


def get_main_set():
    paths = []
    with open('input/input03.txt') as f:
        paths.extend(f.readlines())

    return paths


def get_test_set():
    paths = ['R8,U5,L5,D3', 'U7,R6,D4,L4']

    return paths


def main():
    paths = get_test_set() if TEST else get_main_set()

    coords = [get_coords(p) for p in paths]

    intersections = set(coords[0].keys()) & set(coords[1].keys())

    total_wire = {}
    for inter in intersections:
        x0 = min([x for x in coords[0].keys() if x == inter], key=lambda x: x.n)
        x1 = min([x for x in coords[1].keys() if x == inter], key=lambda x: x.n)

        value = x0.n + x1.n

        if value:
            total_wire[inter] = x0.n + x1.n

    print('Result')
    shortest = min(total_wire.values())

    for k, v in total_wire.items():
        if v == shortest:
            print(k, '->', v)


if __name__ == '__main__':
    main()
