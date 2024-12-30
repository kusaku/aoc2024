from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DIRECTIONS = (('N', (-1, 0)), ('E', (0, 1)), ('S', (1, 0)), ('W', (0, -1)))


def parse_input(filename):
    lines = Path(filename).read_text().strip().splitlines()
    return {
        (r, c): cell
        for r, line in enumerate(lines)
        for c, cell in enumerate(line.strip())
    }


def find_regions(world):
    visited = set()
    regions = []

    for pos, cell in world.items():
        if pos in visited:
            continue

        stack = [pos]
        region = set()
        edges = set()

        while stack:
            pos = stack.pop()

            if pos in visited:
                continue

            visited.add(pos)

            region.add(pos)
            r, c = pos

            for dir_name, (dr, dc), in DIRECTIONS:
                new_pos = r + dr, c + dc
                if world.get(new_pos) != cell:
                    edges.add((dir_name, new_pos))
                elif new_pos not in visited:
                    stack.append(new_pos)

        sides = count_sides(edges)

        regions.append(
            {
                'pos': pos,
                'cell': cell,
                'region': region,
                'area': len(region),
                'edges': edges,
                'perim': len(edges),
                'sides': sides,
                'price1': len(region) * len(edges),
                'price2': len(region) * sides
            }
        )

    return regions


def count_sides(edges: set):
    total_sides = 4

    for dir_name, _ in DIRECTIONS:
        sorted_edges = sorted((r, c) if dir_name in 'NS' else (c, r) for d, (r, c) in edges if d == dir_name)
        total_sides += sum(
            1
                for (r1, c1), (r2, c2) in zip(sorted_edges, sorted_edges[1:])
                if r1 != r2 or abs(c1 - c2) != 1
        )

    return total_sides


def draw_text(draw, region, cell_size, text):
    y = sum(r for r, _ in region) * cell_size // len(region) + cell_size // 2
    x = sum(c for _, c in region) * cell_size // len(region) + cell_size // 2

    font = ImageFont.truetype("arialbd.ttf", 20)  # Arial Bold

    # Draw shadow as outline
    offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (-1, 0), (0, 1), (1, 0)]
    for dx, dy in offsets:
        draw.text((x + dx, y + dy), text, fill="black", font=font, anchor="mm")

    # Draw text
    draw.text((x, y), text, fill="white", font=font, anchor="mm")


def draw_text2(draw, x, y, text):
    font = ImageFont.truetype("arialbd.ttf", 50)  # Arial Bold

    # Draw shadow as outline
    offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (-1, 0), (0, 1), (1, 0)]
    for dx, dy in offsets:
        dx, dy = dx * 2, dy * 3
        draw.text((x + dx, y + dy), text, fill="black", font=font, anchor="mm")

    # Draw text
    draw.text((x, y), text, fill="white", font=font, anchor="mm")


def setup_images(rows, cols, cell_size):
    """Initialize images and drawing contexts."""
    img_area = Image.new('RGB', (cols * cell_size, rows * cell_size), 'black')
    img_perim = Image.new('RGB', (cols * cell_size, rows * cell_size), 'black')
    img_sides = Image.new('RGB', (cols * cell_size, rows * cell_size), 'black')
    return (
        img_area, img_perim, img_sides,
        ImageDraw.Draw(img_area),
        ImageDraw.Draw(img_perim),
        ImageDraw.Draw(img_sides),
    )


def compute_color(value, max_value, color_scheme):
    """Compute color based on value and color scheme."""
    return (
        max(0, min(255, 256 * (value * color_scheme[0]) // max_value)),
        max(0, min(255, 256 * (value * color_scheme[1]) // max_value)),
        max(0, min(255, 256 * (value * color_scheme[2]) // max_value)),
    )


def draw_region(draw, region, cell_size, color):
    """Draw a region on the image."""
    for r, c in region:
        x0, y0 = c * cell_size, r * cell_size
        x1, y1 = x0 + cell_size, y0 + cell_size
        draw.rectangle([x0, y0, x1, y1], fill=color)


def draw_edges(draw, edges, cell_size):
    """Draw edges as lines on the image."""
    for dir_name, (dr, dc) in DIRECTIONS:
        for d, (r, c) in edges:
            if d == dir_name:
                if dir_name == 'W':
                    c += 1
                if dir_name == 'N':
                    r += 1
                x0, y0 = c * cell_size, r * cell_size
                x1, y1 = (x0 + cell_size, y0) if dir_name in "NS" else (x0, y0 + cell_size)
                draw.line([x0, y0, x1, y1], fill='black', width=1)


def process_region(info, draw_area, draw_perim, draw_sides, cell_size, max_values):
    """Process and draw a single region."""
    color_area = compute_color(info['area'], max_values['area'], (2, 2, 0))
    color_perim = compute_color(info['perim'], max_values['perim'], (2, 2, 1))
    color_sides = compute_color(info['sides'], max_values['sides'], (0, 2, 2))

    draw_region(draw_area, info['region'], cell_size, color_area)
    draw_region(draw_perim, info['region'], cell_size, color_perim)
    draw_region(draw_sides, info['region'], cell_size, color_sides)

    draw_edges(draw_area, info['edges'], cell_size)
    draw_edges(draw_perim, info['edges'], cell_size)
    draw_edges(draw_sides, info['edges'], cell_size)

    draw_text(draw_area, info['region'], cell_size, str(info['area']))
    draw_text(draw_perim, info['region'], cell_size, str(info['perim']))
    draw_text(draw_sides, info['region'], cell_size, str(info['sides']))


def part1():
    world = parse_input('my_input.txt')
    regions = find_regions(world)

    cell_size = 10
    rows = max(r for r, _ in world) + 1
    cols = max(c for _, c in world) + 1

    max_values = {
        'area': max(r['area'] for r in regions),
        'perim': max(r['perim'] for r in regions),
        'sides': max(r['sides'] for r in regions)
    }

    img_area, img_perim, img_sides, draw_area, draw_perim, draw_sides = setup_images(rows, cols, cell_size)

    last_progress = 0
    regions_count = len(regions)

    for i, info in enumerate(regions):
        process_region(info, draw_area, draw_perim, draw_sides, cell_size, max_values)

        progress = i * 100 // regions_count
        if progress != last_progress:
            print(f'Progress: {progress}%', end='\r', flush=True)
            last_progress = progress

    print('\r\033[2K', end='\r')

    y = 30
    x = max(c for _, c in world) * cell_size // 2

    draw_text2(draw_area, x, y, 'areas of regions')
    draw_text2(draw_perim, x, y, 'perimeters of regions')
    draw_text2(draw_sides, x, y, 'number of sides in regions')

    img_area.save('day11_area.png')
    img_perim.save('day11_perim.png')
    img_sides.save('day11_sides.png')

    print(f'Answer: {total_cost}')


if __name__ == '__main__':
    part1()
