import math
import sys

import pandas as pd


def read_stdin(file):
    if file is None:
        file = sys.stdin

    df = pd.read_csv(file, header=0)
    return df


class Coord:
    def __init__(self, x, y, n=0, c=None):
        self.x = x
        self.y = y
        self.n = n
        self.c = c

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y, self.n + 1)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y, self.n - 1)

    def __repr__(self):
        return f'({self.x:2d}, {self.y:2d})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __lt__(self, other):
        return self.n < other.n

    def __floordiv__(self, other):
        return Coord(self.x // other, self.y // other)

    @property
    def theta_deg(self):
        if self.x == 0 and self.y == 0:
            return None
        return math.degrees(math.atan2(self.y, self.x))

    @property
    def d(self):
        return abs(self.x) + abs(self.y)
