from pathlib import Path

RED = "\033[31m"
YELLOW = "\033[33m"
WHITE = "\033[37m"
RESET = "\033[0m"


def parse_input(filename):
    grid = [list(line) for line in Path(filename).read_text().strip().splitlines()]

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell in '^>v<':
                guard_x, guard_y = (x, y)
                guard_heading = cell
                grid[x][y] = '.'

    return grid, guard_x, guard_y, guard_heading


def display_grid(grid, guard_x, guard_y, guard_heading, visited):
    grid_copy = [row[:] for row in grid]

    for x, y, heading in visited:
        heading = {'^': '|', '>': '-', 'v': '|', '<': '-'}.get(heading, heading)
        grid_copy[x][y] = f"{YELLOW}{heading}{RESET}"

    grid_copy[guard_x][guard_y] = f"{RED}{guard_heading}{RESET}"
    width = len(grid_copy[0]) * 2 - 1
    horizontal_border = f"{WHITE}+{'-' * width}+{RESET}"

    result = [horizontal_border]
    for row in grid_copy:

        row_display = ' '.join(cell if cell != '.' else ' ' for cell in row)
        result.append(f"{WHITE}|{RESET}{row_display}{WHITE}|{RESET}")
    result.append(horizontal_border)

    print('\n'.join(result))


def simulate_patrol(grid, guard_x, guard_y, guard_heading):
    visited = set()
    moves = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    headings = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

    visited.add((guard_x, guard_y, guard_heading))

    while True:
        dx, dy = moves[guard_heading]
        new_x, new_y = guard_x + dx, guard_y + dy

        if not (0 <= new_x < len(grid) and 0 <= new_y < len(grid[0])):
            break

        if grid[new_x][new_y] == '#':
            guard_heading = headings[guard_heading]
        else:
            guard_x, guard_y = new_x, new_y

        if (guard_x, guard_y, guard_heading) in visited:
            return visited, True

        visited.add((guard_x, guard_y, guard_heading))

    return visited, False


def find_loop_positions(grid, guard_x, guard_y, guard_heading):
    loop_positions = []
    total_cells = len(grid) * len(grid[0])
    processed_cells = 0
    last_percent = 0

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            processed_cells += 1

            percent = processed_cells * 100 // total_cells
            if percent > last_percent:
                print(f'Progress: {percent}%', end='\r', flush=True)
                last_percent = percent

            if (x, y) == (guard_x, guard_y) or cell == '#':
                continue

            grid[x][y] = '#'

            visited, is_loop = simulate_patrol(grid, guard_x, guard_y, guard_heading)

            if is_loop:
                loop_positions.append((x, y, visited))

            grid[x][y] = '.'

    print('\r\033[2K', end='\r')

    sorted_loops = sorted(loop_positions, key=lambda x: len(x[2]))

    for x, y, visited in sorted_loops[0], sorted_loops[-1]:
        grid[x][y] = f"{RED}X{RESET}"
        display_grid(grid, guard_x, guard_y, guard_heading, visited)
        grid[x][y] = '.'

    return loop_positions


def part1():
    grid, guard_x, guard_y, guard_heading = parse_input('my_input.txt')
    visited, _ = simulate_patrol(grid, guard_x, guard_y, guard_heading)
    display_grid(grid, guard_x, guard_y, guard_heading, visited)
    visited_positions = {(x, y) for x, y, _ in visited}
    print(f'Answer: {len(visited_positions)}')


def part2():
    grid, guard_x, guard_y, guard_heading = parse_input('my_input.txt')
    loop_positions = find_loop_positions(grid, guard_x, guard_y, guard_heading)
    print(f'Answer: {len(loop_positions)}')


if __name__ == '__main__':
    part1()
    part2()
