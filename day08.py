
N = 8

W = 25
H = 6


def load_dataset(test=False):
    is_test = '_test' if test else ''
    filename = f'input{N:02d}{is_test}.txt'

    with open(filename) as f:
        pxs = f.readlines()[0]
    return pxs


def get_layered(pxs):
    lc = 0
    i = 0

    layered = []
    while i < len(pxs):
        layer = []
        print('Layer', lc)
        nc = 0
        while nc < H:
            col = [int(c) for c in pxs[i: i + W]]
            print('Col', nc, col)
            layer.extend(col)
            i += W
            nc += 1
        lc += 1
        layered.append(layer)

    return layered


def main():
    pixels = [int(x) for x in load_dataset()]

    layers = get_layered(pixels)

    possible_values = set(pixels)
    values = [get_values_count(layer, possible_values) for layer in layers]
    zeros = [v[0] for v in values]
    index_min = min(range(len(zeros)), key=zeros.__getitem__)

    print(f'Layer {index_min} has {zeros[index_min]} zeros')

    ones = values[index_min][1]
    twos = values[index_min][2]
    print(f'Layer {index_min} has {ones} 1s and {twos} 2s (prod={ones * twos})')

    merged_layer = join_layers(layers)
    print_image(merged_layer)


def join_layers(layers):
    joined = [2] * W * H
    print(joined)
    for layer in layers:
        print('+')
        print(layer)
        for i in range(W * H):
            if joined[i] == 2:
                joined[i] = layer[i]
        print('=')
        print(joined)
    return joined


def print_image(merged_layer):
    image = [get_content(p) for p in merged_layer]
    for c in range(H):
        print(*image[c * W: (c * W) + W], sep='')


def get_content(p):
    if p == 1:
        return '█'
    if p == 0:
        return ' '
    raise ValueError


def get_values_count(layer, values):
    res = {}
    for i in values:
        res[i] = len([n for n in layer if n == i])

    return res


if __name__ == '__main__':
    main()
