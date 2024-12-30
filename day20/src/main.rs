use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};
use std::fs;

type Position = (usize, usize);
const DIRECTIONS: [(isize, isize); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

fn parse_input(filename: &str) -> (Vec<Vec<char>>, Position, Position) {
    let data = fs::read_to_string(filename).expect("Failed to read file");
    let grid: Vec<Vec<char>> = data.trim().lines().map(|line| line.chars().collect()).collect();
    let mut start = None;
    let mut end = None;

    for (r, row) in grid.iter().enumerate() {
        for (c, &cell) in row.iter().enumerate() {
            if cell == 'S' {
                start = Some((r, c));
            } else if cell == 'E' {
                end = Some((r, c));
            }
        }
    }

    (grid, start.unwrap(), end.unwrap())
}

fn find_shortest_path(grid: &[Vec<char>], start: Position, end: Position) -> Vec<Position> {
    let (rows, cols) = (grid.len(), grid[0].len());
    let mut heap = BinaryHeap::new();
    let mut visited = HashMap::new();

    heap.push(Reverse((0, start.0, start.1, vec![start])));

    while let Some(Reverse((cost, r, c, path))) = heap.pop() {
        if *visited.get(&(r, c)).unwrap_or(&usize::MAX) < cost {
            continue;
        }

        visited.insert((r, c), cost);

        if (r, c) == end {
            return path;
        }

        for &(dr, dc) in &DIRECTIONS {
            let nr = (r as isize + dr) as usize;
            let nc = (c as isize + dc) as usize;

            if nr < rows && nc < cols && grid[nr][nc] != '#' {
                let mut new_path = path.clone();
                new_path.push((nr, nc));
                heap.push(Reverse((cost + 1, nr, nc, new_path)));
            }
        }
    }

    vec![]
}

fn part1() {
    let (grid, start, end) = parse_input("my_input.txt");
    let path = find_shortest_path(&grid, start, end);

    let min_savings = 100;
    let path_length = path.len();
    let mut cheat_path_count = 0;

    for i in 0..path_length - 1 {
        print!("\rProgress: {}%", i * 100 / path_length);

        for j in i + 1..path_length {
            let (r1, c1) = path[i];
            let (r2, c2) = path[j];
            let cheat_length = r1.abs_diff(r2) + c1.abs_diff(c2);

            if cheat_length == 2 {
                let savings = j - i - cheat_length;
                if savings >= min_savings {
                    cheat_path_count += 1;
                }
            }
        }
    }

    print!("\r\x1b[2K");

    println!("Answer: {}", cheat_path_count);
}

fn part2() {
    let (grid, start, end) = parse_input("my_input.txt");
    let path = find_shortest_path(&grid, start, end);

    let min_savings = 100;
    let max_cheat_distance = 20;
    let path_length = path.len();
    let mut cheat_path_count = 0;

    for i in 0..path_length - 1 {
        print!("\rProgress: {}%", i * 100 / path_length);

        for j in i + 1..path_length {
            let (r1, c1) = path[i];
            let (r2, c2) = path[j];
            let cheat_distance = (r1 as i32 - r2 as i32).abs() + (c1 as i32 - c2 as i32).abs();

            if cheat_distance <= max_cheat_distance {
                let savings = (j - i) as i32 - cheat_distance;
                if savings >= min_savings {
                    cheat_path_count += 1;
                }
            }
        }
    }

    print!("\r\x1b[2K");

    println!("Answer: {}", cheat_path_count);
}

fn main() {
    part1();
    part2();
}
