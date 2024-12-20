import sys
from heapq import heappop, heappush
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

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


def line_between(a, b):
    (r1, c1), (r2, c2) = a, b
    line = []
    current_r, current_c = r1, c1

    dr = r2 - r1
    dc = c2 - c1

    while current_r != r2:
        line.append((current_r, c2))
        current_r += 1 if dr > 0 else -1

    while current_c != c2:
        line.append((r1, current_c))
        current_c += 1 if dc > 0 else -1

    return line


def draw_grid(grid, start, end, path, all_paths=[], pixel_size=5, text=None):
    rows, cols = len(grid), len(grid[0])
    img = Image.new('RGB', (cols * pixel_size, rows * pixel_size), 'black')
    draw = ImageDraw.Draw(img)

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            x0, y0 = c * pixel_size, r * pixel_size
            x1, y1 = x0 + pixel_size, y0 + pixel_size
            if cell == '#':
                draw.rectangle([x0, y0, x1, y1], fill='gray')

    for r, c in path:
        x0, y0 = c * pixel_size, r * pixel_size
        x1, y1 = x0 + pixel_size, y0 + pixel_size
        draw.rectangle([x0, y0, x1, y1], fill='white')

    for r, c in all_paths:
        x0, y0 = c * pixel_size, r * pixel_size
        x1, y1 = x0 + pixel_size, y0 + pixel_size
        draw.rectangle([x0, y0, x1, y1], fill='cyan')

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

    images = [draw_grid(grid, start, end, path)]

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

                    path_cut = path[0:i] + path[j:-1]
                    shortcut = line_between(path[i], path[j])

                    images.append(
                        draw_grid(grid, path[i], path[j], path_cut, all_paths=shortcut)
                    )

    images[0].save(
        'shortcuts.gif',
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
    )

    sys.stdout.write('\r\033[2K')

    print(f'Answer: {cheat_path_count}')


if __name__ == '__main__':
    # part1()
    part2()
