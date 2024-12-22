from collections import defaultdict
from itertools import pairwise
from pathlib import Path

MASK_24BIT = 0xFFFFFF
GENS = 2000
SEQ_LEN = 4


def part1():
    data = Path('my_input.txt').read_text().strip().splitlines()
    secrets = map(int, data)

    secret_sum = 0
    for secret in secrets:
        for _ in range(GENS):
            secret = ((secret << 6) ^ secret) & MASK_24BIT
            secret = ((secret >> 5) ^ secret) & MASK_24BIT
            secret = ((secret << 11) ^ secret) & MASK_24BIT

        secret_sum += secret

    print("Answer:", secret_sum)


def part2():
    data = Path('my_input.txt').read_text().strip().splitlines()
    secrets = map(int, data)

    amounts = defaultdict(int)
    for secret in secrets:
        digits = []
        for _ in range(GENS):
            secret = ((secret << 6) ^ secret) & MASK_24BIT
            secret = ((secret >> 5) ^ secret) & MASK_24BIT
            secret = ((secret << 11) ^ secret) & MASK_24BIT
            digits.append(secret % 10)

        deltas = [b - a for a, b in pairwise(digits)]
        deltas_windows = (tuple(deltas[i: i + SEQ_LEN]) for i in range(GENS - SEQ_LEN))
        seen_sequences = set()
        for sequence, price in zip(deltas_windows, digits[SEQ_LEN:]):
            if sequence not in seen_sequences:
                seen_sequences.add(sequence)
                amounts[sequence] += price

    print("Answer:", max(amounts.values()))


if __name__ == '__main__':
    part1()
    part2()
