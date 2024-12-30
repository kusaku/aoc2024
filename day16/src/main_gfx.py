from collections import defaultdict
from heapq import heappop, heappush
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_input(filename):
    maze = Path(filename).read_text().strip().splitlines()
    start = end = None
    for r, row in enumerate(maze):
        if 'S' in row:
            start = (r, row.index('S'))
        if 'E' in row:
            end = (r, row.index('E'))
        if start and end:
            break
    return maze, start, end


def draw_maze(maze, start, end, path, all_paths=[], pixel_size=5, text=None):
    rows, cols = len(maze), len(maze[0])
    img = Image.new('RGB', (cols * pixel_size, rows * pixel_size), 'black')
    draw = ImageDraw.Draw(img)

    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            x0, y0 = c * pixel_size, r * pixel_size
            x1, y1 = x0 + pixel_size, y0 + pixel_size
            if cell == '#':
                draw.rectangle([x0, y0, x1, y1], fill='gray')

    for r, c in all_paths:
        x0, y0 = c * pixel_size, r * pixel_size
        x1, y1 = x0 + pixel_size, y0 + pixel_size
        draw.rectangle([x0, y0, x1, y1], fill='cyan')

    for r, c in path:
        x0, y0 = c * pixel_size, r * pixel_size
        x1, y1 = x0 + pixel_size, y0 + pixel_size
        draw.rectangle([x0, y0, x1, y1], fill='white')

    sx0, sy0 = start[1] * pixel_size, start[0] * pixel_size
    sx1, sy1 = sx0 + pixel_size, sy0 + pixel_size
    draw.rectangle([sx0, sy0, sx1, sy1], fill='red')

    ex0, ey0 = end[1] * pixel_size, end[0] * pixel_size
    ex1, ey1 = ex0 + pixel_size, ey0 + pixel_size
    draw.rectangle([ex0, ey0, ex1, ey1], fill='blue')

    if text:
        font = ImageFont.truetype('arialbd.ttf', 30)
        draw.text((15, 5), text, fill='white', font=font)

    return img


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

    images = [draw_maze(maze, start, end, [])]
    drawn = set()

    while heap:
        cost, r, c, direction, path = heappop(heap)

        if cost > best_cost:
            continue

        if visited.get((r, c, direction), float('inf')) < cost:
            continue

        visited[(r, c, direction)] = cost

        if tuple(path) not in drawn:
            images.append(draw_maze(maze, start, end, path))
            drawn.add(tuple(path))

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

    images[0].save(
        f'maze_dijkstra.gif',
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
    )

    return best_paths


def a_star_best_paths(maze, start, end):
    def heuristic1(a, b):
        return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])

    def heuristic2(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def heuristic3(path):
        return -len(path)

    rows, cols = len(maze), len(maze[0])
    heap = [(heuristic2(start, end), 0, start[0], start[1], 0, [start])]
    visited = {}

    best_cost = float('inf')
    best_paths = []

    images = [draw_maze(maze, start, end, [])]
    drawn = set()

    while heap:
        _, cost, r, c, direction, path = heappop(heap)

        if cost > best_cost:
            continue

        if visited.get((r, c, direction), float('inf')) < cost:
            continue

        visited[(r, c, direction)] = cost

        if tuple(path) not in drawn:
            images.append(draw_maze(maze, start, end, path))
            drawn.add(tuple(path))

        if (r, c) == end:
            if cost < best_cost:
                best_cost = cost
                best_paths = [path]
            elif cost == best_cost:
                best_paths.append(path)
            continue

        nr, nc = r + DIRECTIONS[direction][0], c + DIRECTIONS[direction][1]
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
            heappush(heap, (heuristic2((nr, nc), start), cost + 1, nr, nc, direction, path + [(nr, nc)]))

        for new_dir in [(direction - 1) % 4, (direction + 1) % 4]:
            heappush(heap, (heuristic2((r, c), start), cost + 1000, r, c, new_dir, path))

    images[0].save(
        f'maze_astar.gif',
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
    )

    return best_paths


def dfs_best_paths(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    best_cost = float('inf')

    stack = [(start[0], start[1], 0, 0, [start])]
    visited = set()
    paths = defaultdict(list)

    images = [draw_maze(maze, start, end, [])]
    drawn = set()

    while stack:
        r, c, direction, cost, path = stack.pop()

        if tuple(path) in visited:
            continue

        visited.add(tuple(path))

        if cost > best_cost:
            continue

        if tuple(path) not in drawn:
            images.append(draw_maze(maze, start, end, path))
            drawn.add(tuple(path))

        if (r, c) == end:
            paths[cost].append(path)
            continue

        for i, (dr, dc) in enumerate(DIRECTIONS):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#' and (nr, nc) not in path:
                new_cost = cost + (1 if i == direction else 1001)
                new_path = path + [(nr, nc)]
                stack.append((nr, nc, i, new_cost, new_path))

    images[0].save(
        f'maze_dfs.gif',
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
    )

    return paths[min(paths)]


def bfs_best_paths(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    best_cost = float('inf')

    stack = [(start[0], start[1], 0, 0, [start])]
    visited = set()
    paths = defaultdict(list)

    images = [draw_maze(maze, start, end, [])]
    drawn = set()

    while stack:
        r, c, direction, cost, path = stack.pop(0)

        if tuple(path) in visited:
            continue

        visited.add(tuple(path))

        if cost > best_cost:
            continue

        if tuple(path) not in drawn:
            images.append(draw_maze(maze, start, end, path))
            drawn.add(tuple(path))

        if (r, c) == end:
            paths[cost].append(path)
            continue

        for i, (dr, dc) in enumerate(DIRECTIONS):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#' and (nr, nc) not in path:
                new_cost = cost + (1 if i == direction else 1001)
                new_path = path + [(nr, nc)]
                stack.append((nr, nc, i, new_cost, new_path))

    images[0].save(
        f'maze_bfs.gif',
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
    )

    return paths[min(paths)]


def part1():
    maze, start, end = parse_input('my_input.txt')

    best_cost = dijkstra_lowest_cost(maze, start, end)

    img = draw_maze(maze, start, end, [])
    img.save('maze.png')

    print(f'Answer: {best_cost}')


def part2():
    maze, start, end = parse_input('my_input.txt')

    for func in (dijkstra_best_paths, a_star_best_paths, dfs_best_paths, bfs_best_paths):
        best_paths = func(maze, start, end)

    all_paths = set(tile for path in best_paths for tile in path)

    images = []

    for i, path in enumerate(best_paths, start=1):
        img = draw_maze(maze, start, end, path, all_paths=all_paths, text=str(i))
        images.append(img)

    images[0].save(
        f'maze_paths_test.gif',
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
    )

    print(f'Answer: {len(set(tile for path in best_paths for tile in path))}')


if __name__ == '__main__':
    # part1()
    part2()
