from heapq import heappop, heappush
from pathlib import Path

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_maze(input_text):
    maze = input_text.splitlines()
    start = end = None
    for r, row in enumerate(maze):
        if 'S' in row:
            start = (r, row.index('S'))
        if 'E' in row:
            end = (r, row.index('E'))
        if start and end:
            break
    return maze, start, end


def dijkstra_lowest_cost(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    heap = [(0, start[0], start[1], 0)]
    visited = {}

    while heap:
        cost, r, c, direction = heappop(heap)

        if visited.get((r, c, direction), float('inf')) <= cost:
            continue

        visited[(r, c, direction)] = cost

        if (r, c) == end:
            return cost

        nr, nc = r + DIRECTIONS[direction][0], c + DIRECTIONS[direction][1]
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
            heappush(heap, (cost + 1, nr, nc, direction))

        for new_dir in (direction - 1) % 4, (direction + 1) % 4:
            heappush(heap, (cost + 1000, r, c, new_dir))

    return float('inf')


def dijkstra_best_paths(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    heap = [(0, start[0], start[1], 0, [start])]
    visited = {}

    best_cost = float('inf')
    best_paths = []

    while heap:
        cost, r, c, direction, path = heappop(heap)

        if cost > best_cost:
            continue

        if visited.get((r, c, direction), float('inf')) < cost:
            continue

        visited[(r, c, direction)] = cost

        if (r, c) == end:
            if cost < best_cost:
                best_cost = cost
            best_paths.append(path)
            continue

        nr, nc = r + DIRECTIONS[direction][0], c + DIRECTIONS[direction][1]
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
            heappush(heap, (cost + 1, nr, nc, direction, path + [(nr, nc)]))

        for new_dir in (direction - 1) % 4, (direction + 1) % 4:
            heappush(heap, (cost + 1000, r, c, new_dir, path))

    return best_paths


def part1():
    input_text = Path('my_input.txt').read_text().strip()
    maze, start, end = parse_maze(input_text)

    best_cost = dijkstra_lowest_cost(maze, start, end)

    print(f'Answer: {best_cost}')


def part2():
    input_text = Path('my_input.txt').read_text().strip()
    maze, start, end = parse_maze(input_text)

    best_paths = dijkstra_best_paths(maze, start, end)
    result = len(set(tile for path in best_paths for tile in path))

    print(f'Answer: {result}')


if __name__ == '__main__':
    # part1()
    part2()
