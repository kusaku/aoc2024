from functools import cache
from itertools import pairwise, permutations, product
from pathlib import Path

NUM_KEYPAD = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
    '#': (3, 0), '0': (3, 1), 'A': (3, 2),
}
DIR_KEYPAD = {
    '#': (0, 0), '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2),
}


def gen_moves(keypad):
    gap = keypad['#']
    moves = {}

    for src, dst in product(keypad.keys() - {'#'}, repeat=2):
        sp, dp = keypad[src], keypad[dst]
        dr, dc = dp[0] - sp[0], dp[1] - sp[1]

        v_moves = ('v' if dr > 0 else '^') * abs(dr)
        h_moves = ('>' if dc > 0 else '<') * abs(dc)

        valid = []
        for perm in set(permutations(v_moves + h_moves)):
            r, c = sp
            for mv in perm:
                r += {'v': 1, '^': -1}.get(mv, 0)
                c += {'>': 1, '<': -1}.get(mv, 0)
                if (r, c) == gap:
                    break
            else:
                valid.append(''.join(perm) + 'A')

        moves[(src, dst)] = valid

    return moves


def min_moves(code, depth, num_moves, dir_moves):
    @cache
    def recurse(seq, d):
        moves = num_moves if d == 0 else dir_moves
        paths = product(*[moves[(a, b)] for a, b in pairwise('A' + seq)])

        if d == depth:
            return min(sum(map(len, p)) for p in paths)
        return min(sum(recurse(n, d + 1) for n in p) for p in paths)

    return recurse(code, 0)


def part1():
    codes = Path('my_input.txt').read_text().strip().splitlines()
    num_moves, dir_moves = gen_moves(NUM_KEYPAD), gen_moves(DIR_KEYPAD)
    total = sum(min_moves(c, 2, num_moves, dir_moves) * int(c[:-1]) for c in codes)

    print(f'Answer: {total}')


def part2():
    codes = Path('my_input.txt').read_text().strip().splitlines()
    num_moves, dir_moves = gen_moves(NUM_KEYPAD), gen_moves(DIR_KEYPAD)
    total = sum(min_moves(c, 25, num_moves, dir_moves) * int(c[:-1]) for c in codes)

    print(f'Answer: {total}')


if __name__ == '__main__':
    part1()
    part2()
