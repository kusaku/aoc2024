from pathlib import Path


def part1():
    grid = Path('my_input.txt').read_text().strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    word = "XMAS"
    word_length = len(word)
    directions = [
        (0, 1),   # Right
        (1, 0),   # Down
        (0, -1),  # Left
        (-1, 0),  # Up
        (1, 1),   # Diagonal down-right
        (-1, -1), # Diagonal up-left
        (1, -1),  # Diagonal down-left
        (-1, 1)   # Diagonal up-right
    ]

    def matches_word(r, c, dr, dc):
        return (
            0 <= r + dr * (word_length - 1) < rows and 0 <= c + dc * (word_length - 1) < cols
            and
            all(grid[r + i * dr][c + i * dc] == word[i] for i in range(word_length))
        )

    count = sum(
        1
        for dr, dc in directions
        for r in range(rows)
        for c in range(cols)
        if matches_word(r, c, dr, dc)
    )

    print(f"Answer: {count}")


def part2():
    grid = Path('my_input.txt').read_text().strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    patterns = [
        ["M.S", ".A.", "M.S"],
        ["M.M", ".A.", "S.S"],
        ["S.M", ".A.", "S.M"],
        ["S.S", ".A.", "M.M"],
    ]
    pattern_size = 3

    def matches_pattern(r, c):
        for pattern in patterns:
            if all(
                grid[r + dr][c + dc] == pattern[dr][dc]
                for dr in range(pattern_size)
                for dc in range(pattern_size)
                if pattern[dr][dc] != '.'
            ):
                return True

        return False

    count = sum(
        1
        for r in range(rows - pattern_size + 1)
        for c in range(cols - pattern_size + 1)
        if matches_pattern(r, c)
    )

    print(f"Answer: {count}")


if __name__ == "__main__":
    part1()
    part2()
