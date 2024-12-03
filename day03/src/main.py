import re
from pathlib import Path


def part1():
    memory = Path('my_input.txt').read_text()
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'

    total_sum = sum(
        int(match.group(1)) * int(match.group(2))
        for match
        in re.finditer(pattern, memory)
    )

    print(f'Answer: {total_sum}')


def part2():
    memory = Path('my_input.txt').read_text()
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)|(do\(\)|don\'t\(\))'
    mul_enabled = True
    total_sum = 0

    for match in re.finditer(pattern, memory):
        if match.group(1) and match.group(2) and mul_enabled:
            total_sum += int(match.group(1)) * int(match.group(2))
        elif match.group(3):
            mul_enabled = match.group(3) == 'do()'

    print(f'Answer: {total_sum}')


if __name__ == '__main__':
    part1()
    part2()
