import sys
from pathlib import Path

import math


def parse_input(input_text):
    positions, velocities = zip(
        *[
            (
                tuple(map(int, position.split('=')[1].split(','))),
                tuple(map(int, velocity.split('=')[1].split(',')))
            )
            for position, velocity in (line.split(' ') for line in input_text.strip().split('\n'))
        ]
    )

    return list(positions), list(velocities)


def simulate_positions(positions, velocities, width, height, steps):
    return [
        ((px + vx * steps) % width, (py + vy * steps) % height)
        for (px, py), (vx, vy) in zip(positions, velocities)
    ]


def calculate_entropy(positions, width, height):
    total = len(positions)
    row_counts = [sum(1 for _, y in positions if y == row) for row in range(height)]
    col_counts = [sum(1 for x, _ in positions if x == col) for col in range(width)]
    probabilities = [count / total for count in row_counts + col_counts]

    return -sum(p * math.log2(p) for p in probabilities if p > 0)


def calculate_largest_cluster(positions, width, height, bin_size=10):
    grid = {}
    for x, y in positions:
        bin_x, bin_y = x // bin_size, y // bin_size
        grid[(bin_x, bin_y)] = grid.get((bin_x, bin_y), 0) + 1

    return max(grid.values(), default=0)


def compute_safety_factor(positions, width, height):
    half_width, half_height = width // 2, height // 2
    quadrants = [
        sum(1 for x, y in positions if (x < half_width and y < half_height)),
        sum(1 for x, y in positions if (x > half_width and y < half_height)),
        sum(1 for x, y in positions if (x < half_width and y > half_height)),
        sum(1 for x, y in positions if (x > half_width and y > half_height))
    ]

    return math.prod(quadrants)


def part1():
    input_text = Path('my_input.txt').read_text().strip()
    positions, velocities = parse_input(input_text)

    width, height = 101, 103
    steps = 100

    final_positions = simulate_positions(positions, velocities, width, height, steps)
    result = compute_safety_factor(final_positions, width, height)

    print(f'Answer: {result}')


def part2():
    input_text = Path('my_input.txt').read_text().strip()
    positions, velocities = parse_input(input_text)

    width, height = 101, 103
    last_entropy, last_steps = float('inf'), 0

    for steps in range(10_000):
        new_positions = simulate_positions(positions, velocities, width, height, steps)
        entropy = calculate_entropy(new_positions, width, height)
        sys.stdout.write(f'\rsteps={steps}, entropy={entropy}')
        sys.stdout.flush()

        if entropy < last_entropy:
            last_entropy, last_steps = entropy, steps

    print('\r\033[2K', end='')

    print(f'Answer: {last_steps}')


def part3():
    input_text = Path('my_input.txt').read_text().strip()
    positions, velocities = parse_input(input_text)

    width, height = 101, 103
    last_largest_cluster, last_steps = 0, 0

    for steps in range(10_000):
        new_positions = simulate_positions(positions, velocities, width, height, steps)
        largest_cluster = calculate_largest_cluster(new_positions, width, height)
        sys.stdout.write(f'\rsteps={steps}, largest_cluster={largest_cluster}')
        sys.stdout.flush()

        if largest_cluster > last_largest_cluster:
            last_largest_cluster, last_steps = largest_cluster, steps

    print('\r\033[2K', end='')
    print(f'Answer: {last_steps}')


if __name__ == '__main__':
    part1()
    part2()
    part3()
