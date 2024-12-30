from heapq import heappop, heappush
from pathlib import Path


def parse_input(filename):
    return [tuple(map(int, line.split(','))) for line in Path(filename).read_text().strip().splitlines()]


def find_shortest_path(grid, grid_size):
    start = (0, 0)
    target = (grid_size - 1, grid_size - 1)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    visited = [row[:] for row in grid]
    priority_queue = [(0, start, [start])]

    while priority_queue:
        _, (x, y), path = heappop(priority_queue)

        if (x, y) == target:
            return path

        if visited[y][x]:
            continue

        visited[y][x] = True

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and not visited[ny][nx]:
                heappush(priority_queue, (len(path), (nx, ny), path + [(nx, ny)]))

    return []


def part1():
    grid_list = parse_input('my_input.txt')
    grid_size = 71
    byte_limit = 1024

    grid = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    for x, y in grid_list[:byte_limit]:
        grid[y][x] = True

    path = find_shortest_path(grid, grid_size)

    print(f'Answer: {len(path) - 1}')


def part2():
    grid_list = parse_input('my_input.txt')
    grid_size = 71

    grid = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    path = find_shortest_path(grid, grid_size)

    for i, (x, y) in enumerate(grid_list):
        print(f'Progress: {i * 100 // len(grid_list)}%', end='\r', flush=True)

        grid[y][x] = True

        # only re-run simulation if new corrupted position affects the path
        if (x, y) in path:
            path = find_shortest_path(grid, grid_size)

            if not path:
                break

    print('\r\033[2K', end='\r')

    print(f'Answer: {x},{y}')


if __name__ == '__main__':
    part1()
    part2()
