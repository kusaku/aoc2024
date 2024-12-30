from pathlib import Path

EMPTY_SPACE = float('inf')


def defragment(blocks, move_whole_files=False):
    total_blocks = len(blocks)
    last_progress = 0
    search_span_from = 0

    for i in reversed(range(total_blocks)):
        progress = (total_blocks - i) * 100 // total_blocks

        if progress != last_progress:
            print(f'Progress: {progress}%', end='\r', flush=True)
            last_progress = progress

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

    defragment(blocks, move_whole_files=False)

    result = calculate_checksum(blocks)
    print(f'Answer: {result}')


def part2():
    disk_map = Path('my_input.txt').read_text().strip()
    blocks = [
        (i // 2 if i % 2 == 0 else EMPTY_SPACE, int(char))
        for i, char in enumerate(disk_map)
    ]

    defragment(blocks, move_whole_files=True)

    result = calculate_checksum(blocks)
    print(f'Answer: {result}')


if __name__ == '__main__':
    part1()
    part2()
