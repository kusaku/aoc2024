use std::collections::BinaryHeap;
use std::fs;

type Point = (usize, usize);

fn parse_input(filename: &str) -> Vec<Point> {
    fs::read_to_string(filename)
        .expect("Failed to read file")
        .trim()
        .lines()
        .map(|line| {
            let parts: Vec<usize> = line
                .split(',')
                .map(|s| s.parse().unwrap())
                .collect();
            (parts[0], parts[1])
        })
        .collect()
}

fn find_shortest_path(grid: &Vec<Vec<bool>>, grid_size: usize) -> Vec<Point> {
    let start: Point = (0, 0);
    let target: Point = (grid_size - 1, grid_size - 1);
    let directions = [(0, -1), (0, 1), (-1, 0), (1, 0)];

    let mut visited = vec![vec![false; grid_size]; grid_size];
    let mut priority_queue = BinaryHeap::from(vec![(0, start, vec![start])]);

    while let Some((_, (x, y), path)) = priority_queue.pop() {
        if (x, y) == target {
            return path;
        }

        if visited[y][x] {
            continue;
        }

        visited[y][x] = true;

        for &(dx, dy) in &directions {
            let nx = x.wrapping_add(dx as usize);
            let ny = y.wrapping_add(dy as usize);
            if nx < grid_size && ny < grid_size && !visited[ny][nx] && !grid[ny][nx] {
                let mut new_path = path.clone();
                new_path.push((nx, ny));
                priority_queue.push((usize::MAX - new_path.len(), (nx, ny), new_path));
            }
        }
    }

    vec![]
}

fn part1() {
    let grid_list = parse_input("my_input.txt");
    let grid_size = 71;
    let byte_limit = 1024;

    let mut grid = vec![vec![false; grid_size]; grid_size];
    for &(x, y) in &grid_list[..byte_limit] {
        grid[y][x] = true;
    }

    let path = find_shortest_path(&grid, grid_size);

    println!("Answer: {}", path.len() - 1);
}

fn part2() {
    let grid_list = parse_input("my_input.txt");
    let grid_size = 71;

    let mut grid = vec![vec![false; grid_size]; grid_size];
    let mut path = find_shortest_path(&grid, grid_size);

    for (i, &(x, y)) in grid_list.iter().enumerate() {
        print!("\rProgress: {}%", i * 100 / grid_list.len());
        grid[y][x] = true;

        // only re-run simulation if new corrupted position affects the path
        if path.contains(&(x, y)) {
            path = find_shortest_path(&mut grid, grid_size);

            if path.is_empty() {
                print!("\r\x1b[2K");
                println!("Answer: {},{}", x, y);
                break;
            }
        }
    }
}

fn main() {
    part1();
    part2();
}
