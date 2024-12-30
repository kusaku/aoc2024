use std::collections::HashMap;
use std::f64;
use std::fs;

fn parse_input(filename: &str) -> (Vec<(i32, i32)>, Vec<(i32, i32)>) {
    let data = fs::read_to_string(filename).expect("Failed to read file");
    let mut positions = Vec::new();
    let mut velocities = Vec::new();

    for line in data.trim().lines() {
        let parts: Vec<&str> = line.split(' ').collect();
        let position: Vec<i32> = parts[0]
            .split('=')
            .nth(1)
            .unwrap()
            .split(',')
            .map(|x| x.parse().unwrap())
            .collect();
        let velocity: Vec<i32> = parts[1]
            .split('=')
            .nth(1)
            .unwrap()
            .split(',')
            .map(|x| x.parse().unwrap())
            .collect();

        positions.push((position[0], position[1]));
        velocities.push((velocity[0], velocity[1]));
    }

    (positions, velocities)
}

fn simulate_positions(
    positions: &[(i32, i32)],
    velocities: &[(i32, i32)],
    width: i32,
    height: i32,
    steps: i32,
) -> Vec<(i32, i32)> {
    positions
        .iter()
        .zip(velocities.iter())
        .map(|(&(px, py), &(vx, vy))| {
            (
                (px + vx * steps).rem_euclid(width),
                (py + vy * steps).rem_euclid(height),
            )
        })
        .collect()
}


fn calculate_entropy(positions: &[(i32, i32)], width: i32, height: i32) -> f64 {
    let total = positions.len() as f64;

    let row_counts: Vec<i32> = (0..height)
        .map(|row| positions.iter().filter(|&&(_, y)| y == row).count() as i32)
        .collect();

    let col_counts: Vec<i32> = (0..width)
        .map(|col| positions.iter().filter(|&&(x, _)| x == col).count() as i32)
        .collect();

    let probabilities: Vec<f64> = row_counts
        .iter()
        .chain(col_counts.iter())
        .map(|&count| count as f64 / total)
        .filter(|&p| p > 0.0)
        .collect();

    probabilities.iter().map(|&p| -p * p.log2()).sum::<f64>()
}

fn calculate_largest_cluster(positions: &[(i32, i32)], _width: i32, _height: i32, bin_size: i32) -> i32 {
    let mut grid = HashMap::new();

    for &(x, y) in positions {
        let bin_x = x / bin_size;
        let bin_y = y / bin_size;
        *grid.entry((bin_x, bin_y)).or_insert(0) += 1;
    }

    *grid.values().max().unwrap_or(&0)
}

fn compute_safety_factor(positions: &[(i32, i32)], width: i32, height: i32) -> i64 {
    let half_width = width / 2;
    let half_height = height / 2;

    let quadrants = vec![
        positions.iter().filter(|&&(x, y)| x < half_width && y < half_height).count() as i64,
        positions.iter().filter(|&&(x, y)| x > half_width && y < half_height).count() as i64,
        positions.iter().filter(|&&(x, y)| x < half_width && y > half_height).count() as i64,
        positions.iter().filter(|&&(x, y)| x > half_width && y > half_height).count() as i64,
    ];

    quadrants.iter().product()
}

fn part1() {
    let (positions, velocities) = parse_input("my_input.txt");

    let (width, height) = (101, 103);
    let steps = 100;

    let final_positions = simulate_positions(&positions, &velocities, width, height, steps);
    let result = compute_safety_factor(&final_positions, width, height);

    println!("Answer: {}", result);
}

fn part2() {
    let (positions, velocities) = parse_input("my_input.txt");

    let (width, height) = (101, 103);
    let mut last_entropy = f64::INFINITY;
    let mut last_steps = 0;

    for steps in 0..10_000 {
        let new_positions = simulate_positions(&positions, &velocities, width, height, steps);
        let entropy = calculate_entropy(&new_positions, width, height);

        print!("\rsteps={}, entropy={}", steps, entropy);

        if entropy < last_entropy {
            last_entropy = entropy;
            last_steps = steps;
        }
    }

    print!("\r\x1b[2K");

    println!("\rAnswer: {}", last_steps);
}

fn part3() {
    let (positions, velocities) = parse_input("my_input.txt");

    let (width, height) = (101, 103);
    let mut last_largest_cluster = 0;
    let mut last_steps = 0;

    for steps in 0..10_000 {
        let new_positions = simulate_positions(&positions, &velocities, width, height, steps);
        let largest_cluster = calculate_largest_cluster(&new_positions, width, height, 10);

        print!("\rsteps={}, largest_cluster={}", steps, largest_cluster);

        if largest_cluster > last_largest_cluster {
            last_largest_cluster = largest_cluster;
            last_steps = steps;
        }
    }

    print!("\r\x1b[2K");

    println!("\rAnswer: {}", last_steps);
}

fn main() {
    part1();
    part2();
    part3();
}
