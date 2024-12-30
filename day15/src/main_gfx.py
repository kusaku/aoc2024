from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

TRANSLATE = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}


def parse_input(filename, is_wide=False):
    lines = Path(filename).read_text().strip().splitlines()
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


def draw_image(layout, robot_pos, boxes, move_dir, is_wide):
    r_size, c_size = (5, 5)
    rows, cols = len(layout), len(layout[0])
    img = Image.new('RGB', (cols * r_size, rows * c_size), color='black')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arialbd.ttf', r_size)

    for r, row in enumerate(layout):
        for c, char in enumerate(row):
            x0, y0 = c * c_size, r * r_size
            x1, y1 = x0 + c_size, y0 + r_size

            if char == '#':
                draw.rectangle([x0, y0, x1, y1], fill='gray')
            elif frozenset([(r, c)]) in boxes:
                draw.rectangle([x0, y0, x1, y1], fill='cyan')
            elif frozenset([(r, c), (r, c + 1)]) in boxes:
                draw.rectangle([x0, y0, x1, y1], fill='blue')
            elif frozenset([(r, c - 1), (r, c)]) in boxes:
                draw.rectangle([x0, y0, x1, y1], fill='green')
            elif (r, c) == robot_pos:
                draw.ellipse([x0, y0, x1, y1], fill='red')

    draw.text((r_size, c_size), move_dir, fill='white', font=font)
    return img


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


def execute(layout, robot_pos, boxes, moves, is_wide):
    img = draw_image(layout, robot_pos, boxes, '', is_wide)
    images = [img]

    for i, move_dir in enumerate(moves):
        if i % (len(moves) // 100 or 1) == 0:
            print(f'Progress {i * 100 // len(moves)}%', end='\r', flush=True)

        robot_pos = move(layout, boxes, *robot_pos, *DIRECTIONS[move_dir])

        img = draw_image(layout, robot_pos, boxes, move_dir, is_wide)
        images.append(img)

    print('\r\033[2K', end='\r')

    images[0].save(
        f'warehouse_robot_{'part2' if is_wide else 'part1'}.gif',
        save_all=True,
        append_images=images[1:],
        duration=0,
        loop=0,
    )

    return robot_pos, boxes


def calculate_gps(boxes):
    return sum(100 * min(r for r, _ in box) + min(c for _, c in box) for box in boxes)


def part1():
    layout, robot_pos, boxes, moves = parse_input('my_input.txt', is_wide=False)
    robot_pos, boxes = execute(layout, robot_pos, boxes, moves)
    print(f'Answer: {calculate_gps(boxes)}')


def part2():
    layout, robot_pos, boxes, moves = parse_input('my_input.txt', is_wide=True)
    robot_pos, boxes = execute(layout, robot_pos, boxes, moves)
    print(f'Answer: {calculate_gps(boxes)}')


if __name__ == '__main__':
    part1()
    part2()
