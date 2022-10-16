import pandas as pd

CENTER_OF_MASS = 'COM'


class Planet:
    def __init__(self, name, orbiting_around=None):
        self.name = name
        self.orbiting_around = orbiting_around
        self.orbiters = set()

    def __repr__(self):
        if self.orbiting_around is None:
            return f'{self.name} <- {[o.name for o in self.orbiters]}'
        return f'{self.orbiting_around.name} <- {self.name} <- {[o.name for o in self.orbiters]}'


def load_dataset(test=True):
    filename = 'input06_test.txt' if test else 'input06.txt'

    return pd.read_csv(filename, sep=')', header=None, names=['center', 'orbiting'])


def count_orbits(p: Planet):
    if p.orbiting_around is None:
        return 0

    return 1 + count_orbits(p.orbiting_around)


def main():
    com_system = {CENTER_OF_MASS: Planet(CENTER_OF_MASS, None)}

    planets = load_dataset(test=False)
    for _, values in planets.iterrows():
        orbiting_around, name = values

        if name not in com_system:
            com_system[name] = Planet(name)

        if orbiting_around not in com_system:
            com_system[orbiting_around] = Planet(orbiting_around)

        com_system[name].orbiting_around = com_system[orbiting_around]
        com_system[orbiting_around].orbiters.add(com_system[name])

    calculate_total_orbits(com_system)
    calculate_jumps(com_system, 'YOU', 'SAN')
    # print(*com_system.values(), sep='\n')


def calculate_jumps(com_system, a, b):
    orig = com_system[a]
    dest = com_system[b]

    a_ancestors = find_all_ancestors(orig)
    b_ancestors = find_all_ancestors(dest)

    common_planets = set(a_ancestors) & set(b_ancestors)
    print(common_planets)

    total = find_path_between(orig, dest, common_planets)
    print(f'TOTAL JUMPS from {a} to {b}: {total}')


def find_path_between(a, b, vertex):
    iter_p = b
    count = 0

    while iter_p := iter_p.orbiting_around:
        if iter_p in vertex:
            break
        count += 1

    iter_p = a
    while iter_p := iter_p.orbiting_around:
        if iter_p in vertex:
            break
        count += 1

    return count


def find_all_ancestors(x: Planet):
    a = []
    iter = x
    while iter.orbiting_around is not None:
        a.append(iter.orbiting_around)
        iter = iter.orbiting_around
    return a


def calculate_total_orbits(com_system):
    counter = 0
    for p in com_system.values():
        c = count_orbits(p)
        counter += c
        print(f'{p.name} orbits {c}')
    print(f'TOTAL: {counter}')


if __name__ == '__main__':
    main()
