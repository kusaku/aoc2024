from pathlib import Path

DIRECTIONS = (('N', (-1, 0)), ('E', (0, 1)), ('S', (1, 0)), ('W', (0, -1)))


def load_map(filename):
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

        regions.append((pos, cell, region, edges))

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


def part1():
    world = load_map('my_input.txt')
    total_cost = 0

    for pos, cell, region, edges in find_regions(world):
        total_cost += len(region) * len(edges)

    print(f'Answer: {total_cost}')


def part2():
    world = load_map('my_input.txt')
    total_cost = 0

    for pos, cell, region, edges in find_regions(world):
        sides = count_sides(edges)
        total_cost += len(region) * sides

    print(f'Answer: {total_cost}')


if __name__ == '__main__':
    part1()
    part2()
