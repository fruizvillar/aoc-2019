import itertools

N = 12


class Coord3d:
    def __init__(self, components):
        self.components = components

    def __add__(self, other):
        return Coord3d([x + y for x, y in zip(self.components, other.components)])

    def __repr__(self):
        return ', '.join(f'<x{i}={x:3}>' for i, x in enumerate(self.components))

    def __eq__(self, other):
        if isinstance(other, int):
            return all([other == x for x in self.components])
        return all([x == y for x, y in zip(self.components, other.components)])


class Moon:
    def __init__(self, pos, name):
        self.pos = Coord3d(pos)
        self.pos0 = Coord3d(pos)
        self.vel = Coord3d((0, 0, 0))
        self.name = name

    def __repr__(self):
        return f'{self.name:8} (pos={self.pos}, vel={self.vel})'

    @property
    def potential_energy(self):
        return sum([abs(x) for x in self.pos.components])

    @property
    def kinetic_energy(self):
        return sum([abs(x) for x in self.vel.components])

    @property
    def energy(self):
        return self.kinetic_energy * self.potential_energy

    @property
    def cycle_completed(self):
        return self.pos == self.pos0 and self.vel == 0

    def gravity_effect(self, other):
        #print(f'Calculating gravity effect in {self.pos}\'s velocity from {other.pos}')
        delta_vel_self = []
        delta_vel_other = []
        for x, y in zip(self.pos.components, other.pos.components):
            if x == y:
                dvx = 0
            elif x > y:
                dvx = -1
            else:
                dvx = 1
            delta_vel_self.append(dvx)
            delta_vel_other.append(-dvx)

        self.vel += Coord3d(delta_vel_self)
        other.vel += Coord3d(delta_vel_other)

        # print(f'Vel in {self.name} changed in {delta_vel_self} to {self.vel}')
        # print(f'Vel in {other.name} changed in {delta_vel_other} to {other.vel}')

    def apply_velocity(self):
        self.pos += self.vel


class Planet:

    def __init__(self, moons, names):
        self.moons = [Moon(moon, name) for moon, name in zip(moons, names)]
        self.steps = 0
        self.n_dims = len(moons[0])
        self.periods = {}

    def __repr__(self):
        return f'After {self.steps} steps:\n' + '\n'.join(repr(m) for m in self.moons) + '\n' + f'E = {self.energy}\n'

    @property
    def energy(self):
        return sum(m.energy for m in self.moons)

    @property
    def cycle_completed(self):
        return all(m.cycle_completed for m in self.moons)

    def step(self, n=1):
        if n == -1:
            n = 99999999999999

        for i in range(1, n + 1):

            for m0, m1 in itertools.combinations(self.moons, 2):
                m0.gravity_effect(m1)
            for m in self.moons:
                m.apply_velocity()
            self.steps += 1

            for xi in range(self.n_dims):
                coordinate_ok = True
                for m in self.moons:
                    if m.pos.components[xi] != m.pos0.components[xi] or m.vel.components[xi] != 0:
                        coordinate_ok = False
                        break

                if coordinate_ok:
                    if xi not in self.periods:
                        print(f'Coordinate {xi} finished in step {i}')
                        self.periods[xi] = i

                    if len(self.periods) == self.n_dims:
                        lcd = 1
                        for v in self.periods.values():
                            lcd *= v

                        print(f'Analysis completed. Iterations {self.periods.values()}. Forecast: {lcd}')
                        break
            if len(self.periods) == self.n_dims:
                break


def load_dataset(test=False):
    if test:
        return [(-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)]
    return [(14, 2, 8), (7, 4, 10), (1, 17, 16), (-4, -1, 1)]


def main():
    saturn = Planet(load_dataset(), ['Io', 'Europa', 'Ganymede', 'Callisto'])
    print(saturn)

    saturn.step(-1)
    print(saturn)


if __name__ == '__main__':
    main()
