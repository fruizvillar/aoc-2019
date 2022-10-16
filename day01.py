from lib import read_stdin
import pandas as pd


def fuel_from_mass(mass: pd.DataFrame, iter=False):
    empty_mass = mass // 3 - 2  # type: pd.DataFrame
    empty_mass.loc[empty_mass < 0] = 0
    if iter and (empty_mass > 0).any():
        print(mass)
        return empty_mass + fuel_from_mass(empty_mass, iter)

    return 0


if __name__ == '__main__':
    df = read_stdin('input/input01.txt', int)
    fuel = df.apply(lambda m: fuel_from_mass(m, iter=True))  # type: pd.DataFrame
    print(fuel.sum())

if __name__ == '__maint__':
    df = pd.DataFrame([12, 14, 1969, 100756])
    fuel = df.apply(lambda m: fuel_from_mass(m, iter=True))  # type: pd.DataFrame
    print(fuel.sum())
