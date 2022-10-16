import math

from lib import Coord

N = 10


class Sky:
    Asteroid = '#'
    Empty = '.'

    CellSep = ''
    RowSep = '\n'

    def __init__(self, rows):
        self.w, self.h = self.get_sky_size(rows)
        self.asteroids = self.get_asteroids(rows)

    @staticmethod
    def get_sky_size(rows):
        return len(rows[0]), len(rows)

    def get_asteroids(self, rows):
        asteroids = {}
        i = 0
        for n_r, row in enumerate(rows):
            for n_c, value in enumerate(row):
                if value == self.Asteroid:
                    c = Coord(n_c, n_r)
                    asteroids[c] = (Coord(n_c, n_r, c=self.Asteroid))
                    i += 1

        return asteroids

    def get_visible_asteroids(self, orig):
        visible_asteroids = set()
        for asteroid in self.asteroids.values():
            if orig == asteroid:
                continue

            if self.is_in_direct_los(orig, asteroid):
                visible_asteroids.add(asteroid)
        return visible_asteroids

    def is_in_direct_los(self, orig, dest):
        v = simplify_direction(dest - orig)
        iter_coord = orig + v

        while iter_coord != dest:
            # print(f'Iterating {orig} to {dest}: {iter_coord}')
            try:
                iter_asteroid = self.asteroids[iter_coord]
                if iter_asteroid.c == self.Asteroid:
                    # print(f'Asteroid found in {iter_coord}')
                    return False
            except KeyError:
                pass

            iter_coord += v

        return True

    def __repr__(self):
        rows = []
        for r in range(self.h):
            row = []
            for c in range(self.w):
                coord = Coord(c, r)
                char = self.asteroids[coord].c if coord in self.asteroids else self.Empty
                row.extend(f'({char:^3})')

            rows.append(self.CellSep.join(row))

        return self.RowSep.join(rows)

    def get_asteroids_visibility(self):
        return {a: self.get_visible_asteroids(a) for a in self.asteroids.values()}

    def vaporize_n(self, orig, n=None):
        limit = len(self.asteroids) - 1 if n is None else min(n, len(self.asteroids) - 1)
        i = 0
        counter = 0
        latest_vaporized = None

        limit_reached = False
        while not limit_reached:
            i += 1
            targets = [a for a in self.asteroids.values()
                       if self.is_in_direct_los(orig, a) and orig != a and a.c == self.Asteroid]

            sorted_targets = sorted(targets, key=lambda a: self.get_azimuth(orig, a))
            print(f'Round {i}')

            for a in sorted_targets:
                counter += 1
                self.vaporize(a, counter)
                latest_vaporized = a
                if counter >= limit:
                    limit_reached = True
                    break

        return latest_vaporized

    def vaporize(self, a, n=None):
        if n is None:
            print(f'The {a} Asteroid was vaporized')
        else:
            print(f'The {n: 3d}th asteroid to be vaporized is at {a}')

        self.asteroids[a].c = n

    @staticmethod
    def get_azimuth(orig: Coord, dest: Coord):
        diff = dest - orig
        return (90 + diff.theta_deg) % 360


def load_dataset(test=False):
    is_test = '_test' if test else ''
    filename = f'input/input{N:02d}{is_test}.txt'

    with open(filename) as f:
        rows = [n.replace('\n', '') for n in f.readlines()]
    return rows


def simplify_direction(c: Coord):
    if c.x == 0 and c.y == 0:
        return c

    if c.x == 0:
        c.y //= abs(c.y)
        return c
    if c.y == 0:
        c.x //= abs(c.x)
        return c

    return c // math.gcd(c.x, c.y)


def main():
    sky = Sky(load_dataset())
    print(sky)
    print(sky.asteroids)

    n_vis = {k: len(v) for k, v in sky.get_asteroids_visibility().items()}
    max_vis = list({k: v for k, v in sorted(n_vis.items(), key=lambda item: item[1])}.keys())[-1]
    max_vis_n = n_vis[max_vis]
    print(f'The asteroid which has visibility of more other asteroids is {max_vis} ({max_vis_n}).')

    latest_vaporized = sky.vaporize_n(max_vis, 200)
    print(sky)
    print(f'Latest vaporized: {latest_vaporized}, res = {latest_vaporized.x * 100 + latest_vaporized.y}.')


if __name__ == '__main__':
    main()
