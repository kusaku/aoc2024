use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap, HashSet};
use std::fs;

type Position = (usize, usize);
const DIRECTIONS: [(isize, isize); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

fn parse_input(filename: &str) -> (Vec<Vec<char>>, Position, Position) {
    let data = fs::read_to_string(filename).expect("Failed to read file");
    let maze: Vec<Vec<char>> = data.trim().lines().map(|line| line.chars().collect()).collect();
    let mut start = None;
    let mut end = None;

    for (r, row) in maze.iter().enumerate() {
        for (c, &cell) in row.iter().enumerate() {
            if cell == 'S' {
                start = Some((r, c));
            } else if cell == 'E' {
                end = Some((r, c));
            }
        }
    }

    (maze, start.unwrap(), end.unwrap())
}

fn dijkstra_lowest_cost(maze: &[Vec<char>], start: Position, end: Position) -> usize {
    let (rows, cols) = (maze.len(), maze[0].len());
    let mut heap = BinaryHeap::new();
    let mut visited = HashMap::new();

    heap.push(Reverse((0, start.0, start.1, 0)));

    while let Some(Reverse((cost, r, c, direction))) = heap.pop() {
        if *visited.get(&(r, c, direction)).unwrap_or(&usize::MAX) <= cost {
            continue;
        }

        visited.insert((r, c, direction), cost);

        if (r, c) == end {
            return cost;
        }

        let nr = (r as isize + DIRECTIONS[direction].0) as usize;
        let nc = (c as isize + DIRECTIONS[direction].1) as usize;
        if nr < rows && nc < cols && maze[nr][nc] != '#' {
            heap.push(Reverse((cost + 1, nr, nc, direction)));
        }

        for new_dir in [(direction + 3) % 4, (direction + 1) % 4] {
            heap.push(Reverse((cost + 1000, r, c, new_dir)));
        }
    }

    usize::MAX
}

fn dijkstra_best_paths(maze: &[Vec<char>], start: Position, end: Position) -> Vec<Vec<Position>> {
    let (rows, cols) = (maze.len(), maze[0].len());
    let mut heap = BinaryHeap::new();
    let mut visited = HashMap::new();

    let mut best_cost = usize::MAX;
    let mut best_paths = Vec::new();

    heap.push(Reverse((0, start.0, start.1, 0, vec![start])));

    while let Some(Reverse((cost, r, c, direction, path))) = heap.pop() {
        if cost > best_cost {
            continue;
        }

        if *visited.get(&(r, c, direction)).unwrap_or(&usize::MAX) < cost {
            continue;
        }

        visited.insert((r, c, direction), cost);

        if (r, c) == end {
            if cost < best_cost {
                best_cost = cost;
            }
            best_paths.push(path);
            continue;
        }

        let nr = (r as isize + DIRECTIONS[direction].0) as usize;
        let nc = (c as isize + DIRECTIONS[direction].1) as usize;
        if nr < rows && nc < cols && maze[nr][nc] != '#' {
            let mut new_path = path.clone();
            new_path.push((nr, nc));
            heap.push(Reverse((cost + 1, nr, nc, direction, new_path)));
        }

        for new_dir in [(direction + 3) % 4, (direction + 1) % 4] {
            heap.push(Reverse((cost + 1000, r, c, new_dir, path.clone())));
        }
    }

    best_paths
}

fn part1() {
    let (maze, start, end) = parse_input("my_input.txt");

    let best_cost = dijkstra_lowest_cost(&maze, start, end);

    println!("Answer: {}", best_cost);
}

fn part2() {
    let (maze, start, end) = parse_input("my_input.txt");

    let best_paths = dijkstra_best_paths(&maze, start, end);
    let unique_count = best_paths
        .iter()
        .flat_map(|path| path.iter())
        .collect::<HashSet<_>>()
        .len();

    println!("Answer: {}", unique_count);
}

fn main() {
    part1();
    part2();
}
