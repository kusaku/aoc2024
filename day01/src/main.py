from collections import Counter
from pathlib import Path


def parse_input(filename):
    data = Path(filename).read_text().splitlines()
    return zip(*[map(int, line.split()) for line in data])


def part1():
    left_list, right_list = map(sorted, parse_input('my_input.txt'))
    total_distance = sum(abs(l - r) for l, r in zip(left_list, right_list))

    print(f'Answer: {total_distance}')


def part2():
    left_list, right_list = parse_input('my_input.txt')
    right_count = Counter(right_list)
    similarity_score = sum(l * right_count[l] for l in left_list)

    print(f'Answer: {similarity_score}')


if __name__ == '__main__':
    part1()
    part2()
