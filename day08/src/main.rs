use std::collections::{HashMap, HashSet};
use std::fs;

#[derive(Debug)]
struct Antenna {
    x: isize,
    y: isize,
    freq: char,
}

#[derive(Debug)]
struct Grid {
    antennas: Vec<Antenna>,
    width: isize,
    height: isize,
}

fn parse_input(filename: &str) -> Grid {
    let data = fs::read_to_string(filename).expect("Failed to read file");
    let lines: Vec<_> = data.trim().lines().collect();

    Grid {
        antennas: lines
            .iter()
            .enumerate()
            .flat_map(|(y, line)| {
                line.trim()
                    .chars()
                    .enumerate()
                    .filter(|(_, freq)| *freq != '.')
                    .map(move |(x, freq)| Antenna {
                        x: x as isize,
                        y: y as isize,
                        freq,
                    })
            })
            .collect(),
        width: lines.first().map_or(0, |line| line.trim().len() as isize),
        height: lines.len() as isize,
    }
}

fn find_antinodes(grid: &Grid, is_part_two: bool) -> HashSet<(isize, isize)> {
    let mut antinodes = HashSet::new();

    let mut frequency_map: HashMap<char, Vec<&Antenna>> = HashMap::new();
    for antenna in &grid.antennas {
        frequency_map.entry(antenna.freq).or_default().push(antenna);
    }

    for positions in frequency_map.values() {
        for (i, a1) in positions.iter().enumerate() {
            for a2 in positions.iter().skip(i + 1) {
                let dx = a2.x - a1.x;
                let dy = a2.y - a1.y;

                for (heading, start_x, start_y) in [(-1, a1.x, a1.y), (1, a2.x, a2.y)] {
                    let mut step = if is_part_two { 0 } else { heading };

                    loop {
                        let xa = start_x + step * dx;
                        let ya = start_y + step * dy;

                        if xa < 0 || xa >= grid.width || ya < 0 || ya >= grid.height {
                            break;
                        }

                        antinodes.insert((xa, ya));

                        if !is_part_two {
                            break;
                        }

                        step += heading;
                    }
                }
            }
        }
    }

    antinodes
}

fn part1() {
    let grid = parse_input("my_input.txt");
    let antinodes = find_antinodes(&grid, false);
    println!("Answer: {}", antinodes.len());
}

fn part2() {
    let grid = parse_input("my_input.txt");
    let antinodes = find_antinodes(&grid, true);
    println!("Answer: {}", antinodes.len());
}

fn main() {
    part1();
    part2();
}
