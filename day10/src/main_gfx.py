from collections import deque
from pathlib import Path
from random import shuffle

from PIL import Image, ImageDraw


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


def count_unique_trails_with_visualization(topomap, trailhead, frames, pixel_size=6):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    queue = deque([(trailhead, (trailhead,))])
    visited = set()

    if frames:
        image = frames[-1]
    else:
        image = Image.new(
            'RGB',
            (len(topomap[0]) * pixel_size, len(topomap) * pixel_size),
            color=(0, 0, 0)
        )

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

            image = image.copy()
            pixels = image.load()
            for i in range(image.width):
                for j in range(image.height):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = (r * 99 // 100, g * 99 // 100, b * 99 // 100)

            draw = ImageDraw.Draw(image)

            for i in range(len(path) - 1):
                px, py = path[i]
                next_px, next_py = path[i + 1]
                draw.line(
                    [
                        (px * pixel_size + pixel_size // 2, py * pixel_size + pixel_size // 2),
                        (next_px * pixel_size + pixel_size // 2, next_py * pixel_size + pixel_size // 2),
                    ],
                    fill='white',
                    width=pixel_size // 2,
                )

            start_x, start_y = path[0]
            draw.ellipse(
                [
                    (start_x * pixel_size, start_y * pixel_size),
                    (start_x * pixel_size + pixel_size, start_y * pixel_size + pixel_size),
                ],
                fill='red',
            )

            end_x, end_y = path[-1]
            draw.ellipse(
                [
                    (end_x * pixel_size, end_y * pixel_size),
                    (end_x * pixel_size + pixel_size, end_y * pixel_size + pixel_size),
                ],
                fill='blue',
            )

            frames.append(image)

            continue

        for dx, dy in directions:
            next_pos = (x + dx, y + dy)
            if is_valid_move(topomap, current_height, next_pos):
                queue.append((next_pos, path + (next_pos,)))

    return trail_count


def part2_with_gif():
    topomap = parse_input('my_input.txt')
    trailheads = find_trailheads(topomap)
    shuffle(trailheads)

    frames = []
    total_rating = 0

    for i, trailhead in enumerate(trailheads):
        total_rating += count_unique_trails_with_visualization(topomap, trailhead, frames)
        print(f'Progress: {i * 100 // len(trailheads)}%', end='\r', flush=True)

    frames[0].save(
        'part2_visualization.gif',
        save_all=True,
        append_images=frames[1:],
        duration=10,
        loop=0,
    )

    print(f'Answer: {total_rating}')


if __name__ == '__main__':
    part2_with_gif()
