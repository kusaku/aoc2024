from collections import deque
from pathlib import Path


def parse_input(filename):
    return [
        [int(char) if char.isdigit() else None for char in line]
        for line in Path(filename).read_text().strip().splitlines()
    ]


def find_trailheads(topomap):
    return [
        (x, y)
        for y, row in enumerate(topomap)
        for x, value in enumerate(row)
        if value == 0
    ]


def is_valid_move(topomap, current_height, next_pos):
    x, y = next_pos
    return (
        0 <= x < len(topomap[0]) and
        0 <= y < len(topomap) and
        topomap[y][x] is not None and
        topomap[y][x] == current_height + 1
    )


def count_reachable_nines(topomap, trailhead):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    queue = deque([trailhead])
    visited = set()
    reachable_nines = 0

    while queue:
        current_pos = queue.popleft()

        if current_pos in visited:
            continue

        visited.add(current_pos)

        x, y = current_pos
        current_height = topomap[y][x]

        if current_height == 9:
            reachable_nines += 1
            continue

        for dx, dy in directions:
            next_pos = (x + dx, y + dy)
            if is_valid_move(topomap, current_height, next_pos):
                queue.append(next_pos)

    return reachable_nines


def count_unique_trails(topomap, trailhead):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    queue = deque([(trailhead, (trailhead,))])
    visited = set()
    trail_count = 0

    while queue:
        current_pos, path = queue.popleft()

        if path in visited:
            continue

        visited.add(path)

        x, y = current_pos
        current_height = topomap[y][x]

        if current_height == 9:
            trail_count += 1
            continue

        for dx, dy in directions:
            next_pos = (x + dx, y + dy)
            if is_valid_move(topomap, current_height, next_pos):
                queue.append((next_pos, path + (next_pos,)))

    return trail_count


def part1():
    topomap = parse_input('my_input.txt')
    trailheads = find_trailheads(topomap)

    total_score = sum(count_reachable_nines(topomap, trailhead) for trailhead in trailheads)

    print(f'Answer: {total_score}')


def part2():
    topomap = parse_input('my_input.txt')
    trailheads = find_trailheads(topomap)

    total_rating = sum(count_unique_trails(topomap, trailhead) for trailhead in trailheads)

    print(f'Answer: {total_rating}')


if __name__ == '__main__':
    part1()
    part2()
