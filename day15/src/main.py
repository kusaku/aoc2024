import sys
from pathlib import Path

DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

TRANSLATE = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}


def load_data(file_path, is_wide=False):
    lines = Path(file_path).read_text().strip().splitlines()
    layout = []
    moves = ''
    robot_pos = None
    boxes = set()

    for line in lines:
        if line.startswith('#'):
            layout.append(list(''.join(TRANSLATE[char] if is_wide else char for char in line)))
        elif line.startswith(tuple(DIRECTIONS.keys())):
            moves += line.strip()

    for r, row in enumerate(layout):
        for c, char in enumerate(row):
            if char == '@':
                robot_pos = (r, c)
                layout[r][c] = '.'
            elif char == 'O':
                boxes.add(frozenset([(r, c)]))
                layout[r][c] = '.'
            elif char == '[':
                boxes.add(frozenset([(r, c), (r, c + 1)]))
                layout[r][c] = layout[r][c + 1] = '.'

    return layout, robot_pos, boxes, moves


from collections import deque


def move(layout, boxes, r, c, dr, dc):
    rows, cols = len(layout), len(layout[0])
    target_r, target_c = r + dr, c + dc

    if target_r < 0 or target_r >= rows or target_c < 0 or target_c >= cols or layout[target_r][target_c] == '#':
        return r, c

    queue, moved = deque([(target_r, target_c)]), set()

    while queue:
        curr_r, curr_c = queue.popleft()
        for box in {b for b in boxes if (curr_r, curr_c) in b and b not in moved}:
            new_positions = {(br + dr, bc + dc) for br, bc in box}
            if any(nr < 0 or nr >= rows or nc < 0 or nc >= cols or layout[nr][nc] == '#' for nr, nc in new_positions):
                return r, c
            queue.extend(new_positions - {(curr_r, curr_c)})
            moved.add(box)

    if moved:
        boxes.difference_update(moved)
        boxes.update(frozenset((br + dr, bc + dc) for br, bc in box) for box in moved)

    return target_r, target_c


def execute(layout, robot_pos, boxes, moves):
    for i, move_dir in enumerate(moves):
        if i % (len(moves) // 100 or 1) == 0:
            sys.stdout.write(f'\rProgress {i * 100 // len(moves)}%')
            sys.stdout.flush()

        robot_pos = move(layout, boxes, *robot_pos, *DIRECTIONS[move_dir])

    sys.stdout.write('\r\033[2K')
    return robot_pos, boxes


def calculate_gps(boxes):
    return sum(100 * min(r for r, _ in box) + min(c for _, c in box) for box in boxes)


def part1():
    layout, robot_pos, boxes, moves = load_data('my_input.txt', is_wide=False)
    robot_pos, boxes = execute(layout, robot_pos, boxes, moves)
    print(f'Answer: {calculate_gps(boxes)}')


def part2():
    layout, robot_pos, boxes, moves = load_data('my_input.txt', is_wide=True)
    robot_pos, boxes = execute(layout, robot_pos, boxes, moves)
    print(f'Answer: {calculate_gps(boxes)}')


if __name__ == '__main__':
    part1()
    part2()
