from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw


def parse_input(file_path):
    data = Path(file_path).read_text().strip().split('\n')
    antennas = [(x, y, freq) for y, line in enumerate(data) for x, freq in enumerate(line) if freq != '.']
    width, height = len(data[0]), len(data)
    return antennas, width, height


def find_antinodes(antennas, width, height, part_two=False):
    antinodes = defaultdict(list)
    frequency_map = defaultdict(list)

    for x, y, freq in antennas:
        frequency_map[freq].append((x, y))

    for freq, positions in frequency_map.items():
        n = len(positions)

        for i in range(n):
            x1, y1 = positions[i]

            for j in range(i + 1, n):
                x2, y2 = positions[j]
                dx, dy = x2 - x1, y2 - y1

                for heading, start_x, start_y in (-1, x1, y1), (1, x2, y2):
                    step = 0 if part_two else heading

                    while True:
                        xa, ya = start_x + step * dx, start_y + step * dy

                        if not (0 <= xa < width and 0 <= ya < height):
                            break

                        antinodes[(xa, ya)].append(freq)

                        if not part_two:
                            break

                        step += heading

    return antinodes


def blend_colors(colors):
    if not colors:
        return (0, 0, 0)

    r = sum(c[0] for c in colors) // len(colors)
    g = sum(c[1] for c in colors) // len(colors)
    b = sum(c[2] for c in colors) // len(colors)

    return (r, g, b)


def generate_frame(antennas, antinodes, width, height, displayed_antennas, displayed_antinodes):
    scale = 5
    image_width, image_height = width * scale, height * scale
    img = Image.new('RGB', (image_width, image_height), 'black')
    draw = ImageDraw.Draw(img)

    antenna_colors = {}
    base_color = 0
    for x, y, freq in antennas:
        if freq not in antenna_colors:
            antenna_colors[freq] = (
                (base_color * 25 % 256, base_color * 75 % 256, base_color * 125 % 256)
            )
            base_color += 1

    for (x, y), freqs in displayed_antinodes.items():
        colors = [antenna_colors[freq] for freq in freqs]
        blended_color = blend_colors(colors)
        attenuated_color = tuple(int(c * 0.5) for c in blended_color)
        draw.rectangle(
            [x * scale, y * scale, (x + 1) * scale - 1, (y + 1) * scale - 1], fill=attenuated_color
        )

    for x, y, freq in displayed_antennas:
        color = antenna_colors[freq]
        draw.rectangle(
            [x * scale, y * scale, (x + 1) * scale - 1, (y + 1) * scale - 1], fill=color
        )

    return img


def generate_gif_clear_transition(antennas, antinodes, width, height, output_file):
    frames = []
    frequency_map = defaultdict(list)
    for x, y, freq in antennas:
        frequency_map[freq].append((x, y))

    frames.append(generate_frame(antennas, antinodes, width, height, [], defaultdict(list)))

    for freq, antenna_positions in sorted(frequency_map.items()):
        frames.append(generate_frame(antennas, antinodes, width, height, [], defaultdict(list)))

        displayed_antennas = [(x, y, freq) for x, y in antenna_positions]
        frames.append(generate_frame(antennas, antinodes, width, height, displayed_antennas, defaultdict(list)))

        displayed_antinodes = defaultdict(list)

        for (x, y), freqs in antinodes.items():
            if freq in freqs:
                displayed_antinodes[(x, y)].append(freq)

        frames.append(generate_frame(antennas, antinodes, width, height, displayed_antennas, displayed_antinodes))

    frames[0].save(
        output_file,
        save_all=True,
        append_images=frames[1:],
        duration=500,
        loop=0,
    )


def part1():
    antennas, width, height = parse_input('my_input.txt')
    antinodes = find_antinodes(antennas, width, height, part_two=False)
    generate_gif_clear_transition(antennas, antinodes, width, height, 'part1_clear_animation.gif')
    print(f'Answer: {len(antinodes)}')


def part2():
    antennas, width, height = parse_input('my_input.txt')
    antinodes = find_antinodes(antennas, width, height, part_two=True)
    generate_gif_clear_transition(antennas, antinodes, width, height, 'part2_clear_animation.gif')
    print(f'Answer: {len(antinodes)}')


if __name__ == '__main__':
    part1()
    part2()
