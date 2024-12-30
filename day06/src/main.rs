use maplit::hashmap;
use std::collections::{HashMap, HashSet};
use std::fs;
use std::io::{self, Write};

type Grid = Vec<Vec<char>>;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct State {
    x: usize,
    y: usize,
    heading: char,
}

fn parse_input(filename: &str) -> (Grid, usize, usize, char) {
    let data = fs::read_to_string(filename).expect("Failed to read file");
    let mut grid: Grid = data.trim().lines().map(|line| line.chars().collect()).collect();
    let mut guard_x = 0;
    let mut guard_y = 0;
    let mut guard_heading = '^';

    for x in 0..grid.len() {
        for y in 0..grid[x].len() {
            if "^>v<".contains(grid[x][y]) {
                guard_x = x;
                guard_y = y;
                guard_heading = grid[x][y];
                grid[x][y] = '.';
                break;
            }
        }
    }

    (grid, guard_x, guard_y, guard_heading)
}

fn simulate_patrol(
    grid: &Grid,
    guard_x: usize,
    guard_y: usize,
    guard_heading: char,
) -> (HashSet<State>, bool) {
    let moves: HashMap<char, (isize, isize)> = hashmap! {
        '^' => (-1, 0),
        '>' => (0, 1),
        'v' => (1, 0),
        '<' => (0, -1),
    };
    let headings: HashMap<char, char> = hashmap! {
        '^' => '>',
        '>' => 'v',
        'v' => '<',
        '<' => '^',
    };

    let mut visited: HashSet<State> = HashSet::new();
    let mut state = State {
        x: guard_x,
        y: guard_y,
        heading: guard_heading,
    };

    visited.insert(state);

    loop {
        let (dx, dy) = moves[&state.heading];
        let new_x = state.x as isize + dx;
        let new_y = state.y as isize + dy;

        if new_x < 0 || new_x >= grid.len() as isize || new_y < 0 || new_y >= grid[0].len() as isize
        {
            break;
        }

        if grid[new_x as usize][new_y as usize] == '#' {
            state.heading = headings[&state.heading];
        } else {
            state.x = new_x as usize;
            state.y = new_y as usize;
        }

        if visited.contains(&state) {
            return (visited, true);
        }

        visited.insert(state);
    }

    (visited, false)
}

fn find_loop_positions(
    grid: &mut Grid,
    guard_x: usize,
    guard_y: usize,
    guard_heading: char,
) -> Vec<(usize, usize, HashSet<State>)> {
    let total_cells = grid.len() * grid[0].len();
    let mut processed_cells = 0;
    let mut last_percent = 0;
    let mut loop_positions = Vec::new();

    for x in 0..grid.len() {
        for y in 0..grid[0].len() {
            processed_cells += 1;

            let percent = processed_cells * 100 / total_cells;
            if percent > last_percent {
                print!("\rProgress: {}%", percent);
                io::stdout().flush().unwrap();
                last_percent = percent;
            }

            if (x, y) == (guard_x, guard_y) || grid[x][y] == '#' {
                continue;
            }

            grid[x][y] = '#';

            let (visited, is_loop) = simulate_patrol(grid, guard_x, guard_y, guard_heading);
            if is_loop {
                loop_positions.push((x, y, visited));
            }

            grid[x][y] = '.';
        }
    }

    print!("\r\033[2K\r");

    loop_positions
}

fn part1() {
    let (grid, guard_x, guard_y, guard_heading) = parse_input("my_input.txt");
    let (visited, _) = simulate_patrol(&grid, guard_x, guard_y, guard_heading);
    let visited_positions: HashSet<_> = visited.iter().map(|state| (state.x, state.y)).collect();
    println!("Answer: {}", visited_positions.len());
}

fn part2() {
    let (mut grid, guard_x, guard_y, guard_heading) = parse_input("my_input.txt");
    let loop_positions = find_loop_positions(&mut grid, guard_x, guard_y, guard_heading);
    println!("Answer: {}", loop_positions.len());
}

fn main() {
    part1();
    part2();
}
