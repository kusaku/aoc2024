import sys
from heapq import heappop, heappush
from pathlib import Path

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_input(input_text):
    grid = list(map(list, input_text.splitlines()))
    start, end = None, None
    for r, row in enumerate(grid):
        if 'S' in row:
            start = (r, row.index('S'))
        if 'E' in row:
            end = (r, row.index('E'))
        if start and end:
            break
    return grid, start, end


def find_shortest_path(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    heap = [(0, start[0], start[1], [start])]
    visited = {}

    while heap:
        cost, r, c, path = heappop(heap)

        if visited.get((r, c), float('inf')) < cost:
            continue

        visited[(r, c)] = cost

        if (r, c) == end:
            return path

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                heappush(heap, (cost + 1, nr, nc, path + [(nr, nc)]))

    return []


def part1():
    input_text = Path('my_input.txt').read_text().strip()
    grid, start, end = parse_input(input_text)

    path = find_shortest_path(grid, start, end)
    min_savings = 100
    path_length = len(path)
    cheat_path_count = 0

    for i in range(path_length - 1):
        sys.stdout.write(f'\rProgress: {i * 100 // path_length}%')
        sys.stdout.flush()

        for j in range(i + 1, path_length):
            (r1, c1), (r2, c2) = path[i], path[j]

            cheat_length = abs(r1 - r2) + abs(c1 - c2)

            if cheat_length == 2:
                savings = (j - i) - cheat_length
                if savings >= min_savings:
                    cheat_path_count += 1

    sys.stdout.write('\r\033[2K')

    print(f'Answer: {cheat_path_count}')


def part2():
    input_text = Path('test_input.txt').read_text().strip()
    grid, start, end = parse_input(input_text)

    path = find_shortest_path(grid, start, end)
    min_savings = 100
    max_cheat_distance = 20
    path_length = len(path)
    cheat_path_count = 0

    for i in range(path_length - 1):
        sys.stdout.write(f'\rProgress: {i * 100 // path_length}%')
        sys.stdout.flush()

        for j in range(i + 1, path_length):
            (r1, c1), (r2, c2) = path[i], path[j]
            cheat_distance = abs(r1 - r2) + abs(c1 - c2)

            if cheat_distance <= max_cheat_distance:
                savings = j - i - cheat_distance
                if savings >= min_savings:
                    cheat_path_count += 1

    sys.stdout.write('\r\033[2K')

    print(f'Answer: {cheat_path_count}')


if __name__ == '__main__':
    part1()
    part2()
