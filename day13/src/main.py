from pathlib import Path

def parse_machine(file_name):
    return [
        (a1, b1, p1, a2, b2, p2)
        for block in Path(file_name).read_text().strip().split('\n\n')
        for lines in [block.split('\n')]
        for (a1, a2, b1, b2, p1, p2) in [(
            *map(int, lines[0].split('X+')[1].split(', Y+')),
            *map(int, lines[1].split('X+')[1].split(', Y+')),
            *map(int, lines[2].split('X=')[1].split(', Y='))
        )]
    ]

def solve_system(a1, b1, p1, a2, b2, p2):
    d = a1 * b2 - a2 * b1

    if d == 0 or (p1 * b2 - p2 * b1) % d or (a1 * p2 - a2 * p1) % d:
        return None

    x, y = (p1 * b2 - p2 * b1) // d, (a1 * p2 - a2 * p1) // d

    return (x, y) if x >= 0 and y >= 0 else None

def part1():
    machines, total_cost = parse_machine('my_input.txt'), 0

    for i, (a1, b1, p1, a2, b2, p2) in enumerate(machines, 1):
        solution = solve_system(a1, b1, p1, a2, b2, p2)

        if solution:
            total_cost += solution[0] * 3 + solution[1]

        print(f'\rProgress: {i * 100 // len(machines)}%', end='')

    print('\r', end='')

    print(f'Answer: {total_cost}')

def part2():
    machines, total_cost = parse_machine('my_input.txt'), 0

    offset = 10_000_000_000_000

    for i, (a1, b1, p1, a2, b2, p2) in enumerate(machines, 1):
        solution = solve_system(a1, b1, p1 + offset, a2, b2, p2 + offset)

        if solution:
            total_cost += solution[0] * 3 + solution[1]

        print(f'\rProgress: {i * 100 // len(machines)}%', end='')

    print('\r', end='')

    print(f'Answer: {total_cost}')

def main():
    part1()
    part2()

if __name__ == '__main__':
    main()
