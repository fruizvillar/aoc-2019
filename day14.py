import numpy as np

N = 14

INPUT = 'ORE'
OUTPUT = 'FUEL'

PART_ONE = False



class Element:
    def __init__(self, reaction):
        try:
            inputs, output = reaction.split('=>')
        except ValueError:
            inputs = None
            output = f'1 {INPUT}'

        result_amount, name = output.strip().split(' ')
        self.name = name.strip()
        self.n = int(result_amount)
        self.inputs = {}
        self.inputs_obj = {}

        if inputs:
            for p in inputs.split(','):
                amount, element = p.strip().split(' ')
                self.inputs[element] = int(amount)

    def __repr__(self):
        return f'{self.name:5}'
        return f'{self.n} {self.name} <= {", ".join([f"{v} {k}" for k, v in self.inputs.items()])}'


def load_dataset(test=False):
    test_str = '_test' if test else ''
    filename = f'input/input{N}{test_str}.txt'

    with open(filename) as f:
        return f.readlines()


def solve_backwards(elements, laboratory, n_out=1):
    laboratory[OUTPUT] += n_out
    laboratory[INPUT] = 0

    # print(*elements.values(), sep='\n')

    last_skipped = []
    while set(k for k, v in laboratory.items() if v > 0) != {INPUT}:
        for name_out, amount_out in laboratory.items():
            if amount_out <= 0 or name_out == INPUT:
                continue

            if amount_out < elements[name_out].n:
                if name_out not in last_skipped:
                    last_skipped.append(name_out)
                    continue
                else:
                    last_skipped.remove(name_out)
                amount_out = elements[name_out].n  # Wasting

            amount_out = min(amount_out, elements[name_out].n)
            # print(f'Checking inputs needed for {amount_out} of {name_out}')

            for name_input, amount_input in elements[name_out].inputs.items():
                laboratory[name_input] += amount_input

                # print(f'For getting {amount_out} of {name_out}, {amount_input} of {name_input} will be used.')

            laboratory[name_out] -= amount_out
            # print(last_skipped, laboratory)
    return laboratory


def solve(elements, laboratory):
    input_amount = 1000000000000
    output_amount = 0

    laboratory[INPUT] += input_amount

    critical_path = {}

    out = elements[OUTPUT]
    critical_path[out] = 1
    print(out, out.n)
    for el, el_n in out.inputs_obj.items():
        print(el, '|', el_n)
        critical_path[el] += el_n

    print(critical_path)
    return laboratory


def main():
    elements = {}

    reactions = load_dataset()

    for reaction in reactions:
        e = Element(reaction)
        elements[e.name] = e
    elements[INPUT] = Element(INPUT)

    for e in elements.values():
        for inp in e.inputs:
            e.inputs_obj[elements[inp]] = e.inputs[inp]

    laboratory = {k: 0 for k in elements.keys()}

    laboratory = solve_backwards(elements, laboratory) if PART_ONE else solve(elements, laboratory)
    print(laboratory)


if __name__ == '__main__':
    main()
