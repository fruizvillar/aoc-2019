TEST = True


def has_adjacent_repetitions(n):
    digits = str(n)

    for d in set(digits):
        repeats = digits.replace(d, 'x', 6)
        if 'xx' in repeats and 'xxx' not in repeats:
            ok = True
            break
    else:
        ok = False
    print(n, ok)
    return ok


def digits_not_decrease(n):
    digits = str(n)
    ok = int(''.join(sorted(digits))) == n
    return ok


def all_happen(fs, n):
    for func in fs:
        if not func(n):
            return False
    return True


def main():
    values = []
    functions = [has_adjacent_repetitions, digits_not_decrease]

    for n in range(356260, 846304):
        if all_happen(functions, n):
            values.append(n)
    print(len(values), values)
    print(min(values), max(values))


if __name__ == '__main__':
    main()
