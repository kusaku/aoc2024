use std::fs;

struct Grid {
    data: Vec<Vec<char>>,
    rows: usize,
    cols: usize,
}

impl Grid {
    fn new(grid_input: &str) -> Self {
        let data: Vec<Vec<char>> = grid_input
            .lines()
            .map(|line| line.chars().collect())
            .collect();
        let rows = data.len();
        let cols = data[0].len();
        Self { data, rows, cols }
    }

    fn count_word_matches(&self, word: &[char]) -> usize {
        let directions = [
            (0, 1),   // Right
            (1, 0),   // Down
            (0, -1),  // Left
            (-1, 0),  // Up
            (1, 1),   // Diagonal down-right
            (-1, -1), // Diagonal up-left
            (1, -1),  // Diagonal down-left
            (-1, 1),  // Diagonal up-right
        ];
        let word_length = word.len();
        let mut count = 0;

        for &(dr, dc) in &directions {
            for r in 0..self.rows {
                for c in 0..self.cols {
                    'check_word: {
                        for i in 0..word_length {
                            let nr = r as isize + dr * i as isize;
                            let nc = c as isize + dc * i as isize;

                            if nr < 0
                                || nc < 0
                                || nr >= self.rows as isize
                                || nc >= self.cols as isize
                            {
                                break 'check_word;
                            }

                            if self.data[nr as usize][nc as usize] != word[i] {
                                break 'check_word;
                            }
                        }

                        count += 1;
                    }
                }
            }
        }

        count
    }

    fn count_pattern_matches(&self, patterns: &[Grid]) -> usize {
        let mut count = 0;

        for pattern in patterns {
            for r in 0..=(self.rows - pattern.rows) {
                for c in 0..=(self.cols - pattern.cols) {
                    'check_pattern: {
                        for dr in 0..pattern.rows {
                            for dc in 0..pattern.cols {
                                let nr = r + dr;
                                let nc = c + dc;

                                if pattern.data[dr][dc] != '.'
                                    && self.data[nr][nc] != pattern.data[dr][dc]
                                {
                                    break 'check_pattern;
                                }
                            }
                        }
                        count += 1;
                    }
                }
            }
        }

        count
    }
}

fn part1() {
    let grid_input = fs::read_to_string("my_input.txt").expect("Error reading file");
    let grid = Grid::new(&grid_input);
    let word: Vec<char> = "XMAS".chars().collect();
    let count = grid.count_word_matches(&word);
    println!("Answer: {}", count);
}

fn part2() {
    let grid_input = fs::read_to_string("my_input.txt").expect("Error reading file");
    let grid = Grid::new(&grid_input);
    let patterns = vec![
        Grid::new("M.S\n.A.\nM.S"),
        Grid::new("M.M\n.A.\nS.S"),
        Grid::new("S.M\n.A.\nS.M"),
        Grid::new("S.S\n.A.\nM.M"),
    ];

    let count = grid.count_pattern_matches(&patterns);
    println!("Answer: {}", count);
}

fn part1_as_2() {
    let grid_input = fs::read_to_string("my_input.txt").expect("Error reading file");
    let grid = Grid::new(&grid_input);
    let patterns = vec![
        Grid::new("XMAS"),                   // Horizontal left-to-right
        Grid::new("SAMX"),                   // Horizontal right-to-left
        Grid::new("X\nM\nA\nS"),             // Vertical top-to-bottom
        Grid::new("S\nA\nM\nX"),             // Vertical bottom-to-top
        Grid::new("X...\n.M..\n..A.\n...S"), // Diagonal top-left to bottom-right
        Grid::new("S...\n.A..\n..M.\n...X"), // Diagonal bottom-right to top-left
        Grid::new("...X\n..M.\n.A..\nS..."), // Diagonal top-right to bottom-left
        Grid::new("...S\n..A.\n.M..\nX..."), // Diagonal bottom-left to top-right
    ];

    let count = grid.count_pattern_matches(&patterns);
    println!("Answer: {}", count);
}

fn main() {
    part1();
    part2();
    part1_as_2();
}
