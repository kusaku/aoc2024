from pathlib import Path

import math
from PIL import Image

EMPTY_SPACE = float('inf')


def defragment(blocks, move_whole_files=False, frames=None):
    total_blocks = len(blocks)
    last_progress = 0
    search_span_from = 0

    for i in reversed(range(total_blocks)):
        progress = (total_blocks - i) * 100 // total_blocks

        if progress != last_progress:
            print(f'Progress: {progress}%', end='\r', flush=True)
            last_progress = progress

            if frames is not None:
                frames.append(generate_frame(blocks))

        file_id, file_length = blocks[i]
        if file_id != EMPTY_SPACE:
            for k in range(search_span_from, i):
                span_id, span_length = blocks[k]

                if span_id == EMPTY_SPACE and span_length >= file_length:
                    blocks[k] = (file_id, file_length)
                    blocks[i] = (span_id, file_length)

                    if span_length > file_length:
                        blocks.insert(k + 1, (span_id, span_length - file_length))
                        total_blocks += 1

                    if not move_whole_files:
                        search_span_from = k

                    break

    print('\r\033[2K', end='\r')


def generate_frame(blocks, scale_factor=2):
    total_length = sum(length for _, length in blocks)
    grid_size = math.ceil(math.sqrt(total_length))

    def block_id_to_color(block_id):
        if block_id == EMPTY_SPACE:
            return (0, 0, 0)
        return (
            64 + int(block_id) * 11 % 192,
            64 + int(block_id) * 37 % 192,
            64 + int(block_id) * 59 % 192
        )

    flat_blocks = []
    for block_id, length in blocks:
        flat_blocks.extend([block_id] * length)

    image = Image.new('RGB', (grid_size, grid_size), 'black')
    for idx, block_id in enumerate(flat_blocks):
        x, y = divmod(idx, grid_size)
        if x < grid_size and y < grid_size:
            image.putpixel((y, x), block_id_to_color(block_id))

    scaled_size = (grid_size * scale_factor, grid_size * scale_factor)
    image = image.resize(scaled_size, Image.NEAREST)

    return image


def save_gif(frames, filename, duration=100):
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
    print(f'GIF saved as: {filename}')


def calculate_checksum(blocks):
    return sum(
        position * block
            for position, block
            in enumerate(span[0] for span in blocks for _ in range(span[1]))
            if block != EMPTY_SPACE
    )


def part1():
    disk_map = Path('my_input.txt').read_text().strip()
    blocks = [
        (i // 2 if i % 2 == 0 else EMPTY_SPACE, 1)
        for i, char in enumerate(disk_map)
        for _ in range(int(char))
    ]

    frames = [generate_frame(blocks)]
    defragment(blocks, move_whole_files=False, frames=frames)
    save_gif(frames, 'part1_animation.gif')

    result = calculate_checksum(blocks)
    print(f'Answer: {result}')


def part2():
    disk_map = Path('my_input.txt').read_text().strip()
    blocks = [
        (i // 2 if i % 2 == 0 else EMPTY_SPACE, int(char))
        for i, char in enumerate(disk_map)
    ]

    frames = [generate_frame(blocks)]
    defragment(blocks, move_whole_files=True, frames=frames)
    save_gif(frames, 'part2_animation.gif')

    result = calculate_checksum(blocks)
    print(f'Answer: {result}')


if __name__ == '__main__':
    part1()
    part2()
