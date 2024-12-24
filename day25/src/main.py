from pathlib import Path

def part1():
    data = Path('my_input.txt').read_text().strip().split("\n\n")
    locks, keys = [], []

    for schematic in data:
        rows = schematic.splitlines()
        heights = [sum(row[col] == "#" for row in rows) - 1 for col in range(len(rows[0]))]
        (locks if all(cell == "#" for cell in rows[0]) else keys).append(heights)

    fitting_pairs_count = sum(
        all(l + k <= 5 for l, k in zip(lock, key))
            for lock in locks
            for key in keys
    )

    print(f'Answer: {fitting_pairs_count}')

if __name__ == '__main__':
    part1()
