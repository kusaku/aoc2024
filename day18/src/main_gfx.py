from heapq import heappop, heappush
from pathlib import Path

from PIL import Image, ImageDraw


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


def draw_grid(grid, start, end, path, new_pixel=None, pixel_size=5):
    rows, cols = len(grid), len(grid[0])
    img = Image.new('RGB', (cols * pixel_size, rows * pixel_size), 'black')
    draw = ImageDraw.Draw(img)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            x0, y0 = x * pixel_size, y * pixel_size
            x1, y1 = x0 + pixel_size, y0 + pixel_size
            if cell:
                draw.rectangle([x0, y0, x1, y1], fill='gray')

    for x, y in path:
        x0, y0 = x * pixel_size, y * pixel_size
        x1, y1 = x0 + pixel_size, y0 + pixel_size
        draw.rectangle([x0, y0, x1, y1], fill='white')

    sx0, sy0 = start[0] * pixel_size, start[1] * pixel_size
    sx1, sy1 = sx0 + pixel_size, sy0 + pixel_size
    draw.rectangle([sx0, sy0, sx1, sy1], fill='red')

    ex0, ey0 = end[0] * pixel_size, end[1] * pixel_size
    ex1, ey1 = ex0 + pixel_size, ey0 + pixel_size
    draw.rectangle([ex0, ey0, ex1, ey1], fill='blue')

    if new_pixel:
        ex0, ey0 = new_pixel[0] * pixel_size, new_pixel[1] * pixel_size
        ex1, ey1 = ex0 + pixel_size, ey0 + pixel_size
        draw.rectangle([ex0, ey0, ex1, ey1], fill='magenta')

    return img


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
    images = [draw_grid(grid, (0, 0), (70, 70), path)]

    for i, (x, y) in enumerate(grid_list):
        print(f'Progress: {i * 100 // len(grid_list)}%', end='\r', flush=True)

        grid[y][x] = True

        # only re-run simulation if new corrupted position affects the path
        if (x, y) in path:
            path = find_shortest_path(grid, grid_size)
            images.append(draw_grid(grid, (0, 0), (70, 70), path))

            if not path:
                break

    print('\r\033[2K', end='\r')

    images[0].save(
        f'grid_paths.gif',
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
    )

    print(f'Answer: {x},{y}')


if __name__ == '__main__':
    part1()
    part2()
