from collections import defaultdict
from pathlib import Path


def parse_input(file_path):
    data = Path(file_path).read_text().strip().split('\n')
    antennas = [(x, y, freq) for y, line in enumerate(data) for x, freq in enumerate(line) if freq != '.']
    width, height = len(data[0]), len(data)
    return antennas, width, height


def find_antinodes(antennas, width, height, part_two=False):
    antinodes = set()
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

                        antinodes.add((xa, ya))

                        if not part_two:
                            break

                        step += heading

    return antinodes


def part1():
    antennas, width, height = parse_input('my_input.txt')
    antinodes = find_antinodes(antennas, width, height, part_two=False)
    print(f'Answer: {len(antinodes)}')


def part2():
    antennas, width, height = parse_input('my_input.txt')
    antinodes = find_antinodes(antennas, width, height, part_two=True)
    print(f'Answer: {len(antinodes)}')


if __name__ == '__main__':
    part1()
    part2()
