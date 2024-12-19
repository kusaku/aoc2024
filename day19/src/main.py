from pathlib import Path


def count_segmentations(string, segments, memo={'': 1}):
    if string in memo:
        return memo[string]

    count = memo[string] = sum(
        count_segmentations(string[len(segment):], segments, memo)
        for segment in segments
        if string.startswith(segment)
    )

    return count


def part1():
    input_data = Path('my_input.txt').read_text().strip()
    patterns, designs = input_data.split('\n\n')

    patterns = patterns.split(', ')
    designs = designs.split('\n')

    possible_count = sum(count_segmentations(design, patterns) > 0 for design in designs)

    print(f'Answer: {possible_count}')


def part2():
    input_data = Path('my_input.txt').read_text().strip()
    patterns, designs = input_data.split('\n\n')

    patterns = patterns.split(', ')
    designs = designs.split('\n')

    total_ways = sum(count_segmentations(design, patterns) for design in designs)

    print(f'Answer: {total_ways}')


if __name__ == '__main__':
    part1()
    part2()
