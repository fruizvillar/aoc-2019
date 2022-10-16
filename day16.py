import itertools
from datetime import datetime

import numpy as np

N = 16

BASE_PATTERN = [0, 1, 0, -1]

N_REPEAT = 10000

N_MESSAGE_OFFSET = 7


def timeit(f):
    def f_timed(*args, **kwargs):
        t0 = datetime.now()
        f(*args, **kwargs)
        delta = datetime.now() - t0
        print(delta)

    return f_timed


def _get_string(test=False):
    if test:
        return '03081770884921959731165446850517' * 500

    return '59738476840592413842278931183278699191914982551989' \
           '91721762740083043049175206419544302803973811178894' \
           '03837901879923493386692168822183622003043049997236' \
           '24146472831445016914494176940890353790253254035638' \
           '36109105856293688476217978095707967320421060264344' \
           '26032131815386260424701334548358241286629525799745' \
           '87126896226949714610624975813583386749314141495655' \
           '81621556813639285288852575424720102138351622821417' \
           '16601118265244213847587834002200171480223326947993' \
           '23429711845103305784628923350853888186977670136593' \
           '06760403350781293277818378647920707222623670535577' \
           '82457012874813963648263589034095952007116785775064' \
           '95998876303181569252680220083046665757597971122614'


def _get_pattern_gen(pos, n=None):
    digits_iterator = (itertools.repeat(p, pos + 1) for p in BASE_PATTERN)
    it = itertools.cycle(itertools.chain(*digits_iterator))
    next(it)  # dropping 1st
    if n:
        return it
    else:
        return itertools.islice(it, n)


def _make_fft_iteration(input_signal, pos):
    total = sum((x * y for x, y in zip(input_signal, _get_pattern_gen(pos))))
    last_unit = abs(total) % 10
    return last_unit


def _make_fft_iterations(input_signal):
    t0 = datetime.now()
    iterate_signal_count, iterate_signal_iterate = itertools.tee(input_signal)
    length = len(list(iterate_signal_count))
    iters_signal = itertools.tee(iterate_signal_iterate, length)

    result = (_make_fft_iteration(iter_signal_i, i) for i, iter_signal_i in enumerate(iters_signal))

    print('Iters took', datetime.now() - t0)
    return result


def _multiply_by_iter_matrix(v, m):
    res = np.zeros(len(m))

    for v_i in v:
        partial_res = [v_i * next(m[j]) for j in range(len(res))]
        res += partial_res

    return (abs(r) % 10 for r in res)


def _get_input(test=False):
    return (int(s) for s in _get_string(test))


def _get_n_phases(input_signal, n):
    result = input_signal
    for p in range(1, n + 1):
        result = _make_fft_iterations(result)
        print(f'After {p:3} phases: {result}')
    return result


def main():
    iter_name, iter_prog = itertools.tee(_get_input(test=True))
    input_str = ''.join(str(x) for x in list(iter_name))
    message_pointer = int(input_str[:N_MESSAGE_OFFSET])
    print('Input signal:', message_pointer)
    res = _get_n_phases(iter_prog, 100)
    print('Result = ', *res, sep='')
    print('Result[pointer:pointer+8] =  ', *res[message_pointer:message_pointer + 8], sep='')


if __name__ == '__main__':
    main()
