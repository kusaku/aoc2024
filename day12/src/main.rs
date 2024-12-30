use itertools::Itertools;
use std::collections::{HashMap, HashSet};
use std::fs;

type Pos = (i32, i32);
type EdgeSet = HashSet<(char, Pos)>;
type Region = (Pos, char, HashSet<Pos>, EdgeSet);

const DIRECTIONS: [(char, Pos); 4] = [('N', (-1, 0)), ('E', (0, 1)), ('S', (1, 0)), ('W', (0, -1))];

fn parse_input(filename: &str) -> HashMap<Pos, char> {
    fs::read_to_string(filename).expect("Failed to read file")
        .trim()
        .lines()
        .enumerate()
        .flat_map(|(r, line)| {
            line.chars()
                .enumerate()
                .map(move |(c, cell)| ((r as i32, c as i32), cell))
        })
        .collect()
}

fn find_regions(world: &HashMap<Pos, char>) -> Vec<Region> {
    let mut visited = HashSet::new();
    let mut regions = Vec::new();

    for (&pos, &cell) in world {
        if visited.contains(&pos) {
            continue;
        }

        let mut stack = vec![pos];
        let mut region = HashSet::new();
        let mut edges = HashSet::new();

        while let Some(pos) = stack.pop() {
            if visited.contains(&pos) {
                continue;
            }

            visited.insert(pos);
            region.insert(pos);
            let (r, c) = pos;

            for &(dir_name, (dr, dc)) in &DIRECTIONS {
                let new_pos = (r + dr, c + dc);
                if world.get(&new_pos) != Some(&cell) {
                    edges.insert((dir_name, new_pos));
                } else if !visited.contains(&new_pos) {
                    stack.push(new_pos);
                }
            }
        }

        regions.push((pos, cell, region, edges));
    }

    regions
}

fn count_sides(edges: &EdgeSet) -> usize {
    let mut total_sides = 4;

    for &(dir_name, _) in &DIRECTIONS {
        total_sides += edges
            .iter()
            .filter(|&&(d, _)| d == dir_name)
            .map(|&(_, (r, c))| {
                if dir_name == 'N' || dir_name == 'S' {
                    (r, c)
                } else {
                    (c, r)
                }
            })
            .sorted_unstable()
            .collect::<Vec<Pos>>()
            .windows(2)
            .filter(|w| {
                let (r1, c1) = w[0];
                let (r2, c2) = w[1];
                r1 != r2 || (c1 - c2).abs() != 1
            })
            .count();
    }

    total_sides
}

fn part1() {
    let world = parse_input("my_input.txt");
    let mut total_cost = 0;

    for (_, _, region, edges) in find_regions(&world) {
        total_cost += region.len() * edges.len();
    }

    println!("Answer: {}", total_cost);
}

fn part2() {
    let world = parse_input("my_input.txt");
    let mut total_cost = 0;

    for (_, _, region, edges) in find_regions(&world) {
        let sides = count_sides(&edges);
        total_cost += region.len() * sides;
    }

    println!("Answer: {}", total_cost);
}

fn main() {
    part1();
    part2();
}
