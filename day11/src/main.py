from collections import Counter
from pathlib import Path


def blink(stone_counts):
    updated_counts = Counter()

    for stone, count in stone_counts.items():
        if stone == 0:
            result = [1]
        elif len(str(stone)) % 2 == 0:
            stone_str = str(stone)
            mid = len(stone_str) // 2
            result = [int(stone_str[:mid]), int(stone_str[mid:])]
        else:
            result = [stone * 2024]

        for new_stone in result:
            updated_counts[new_stone] += count

    return updated_counts


def count_stones(initial, blinks):
    stone_counts = Counter(initial)

    for i in range(blinks):
        stone_counts = blink(stone_counts)
        print(f'Progress: {i * 100 // blinks}%', end='\r', flush=True)

    print('\r\033[2K', end='\r')

    return sum(stone_counts.values())


def part1():
    data = Path('my_input.txt').read_text().strip()
    initial = list(map(int, data.split()))
    result = count_stones(initial, 25)

    print(f'Answer: {result}')


def part2():
    data = Path('my_input.txt').read_text().strip()
    initial = list(map(int, data.split()))
    result = count_stones(initial, 75)

    print(f'Answer: {result}')


def part3():
    input_data = Path('my_input.txt').read_text().strip()
    initial = list(map(int, input_data.split()))
    result = count_stones(initial, 1000)

    print(f'Answer: {result}')


if __name__ == '__main__':
    part1()
    part2()
    part3()
