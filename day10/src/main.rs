use std::collections::{HashSet, VecDeque};
use std::fs;

type Topomap = Vec<Vec<Option<u32>>>;

fn parse_map(input_text: &str) -> Topomap {
    input_text
        .lines()
        .map(|line| line.chars().map(|c| c.to_digit(10)).collect())
        .collect()
}

fn find_trailheads(topomap: &Topomap) -> Vec<(usize, usize)> {
    let mut trailheads = Vec::new();
    for (y, row) in topomap.iter().enumerate() {
        for (x, &value) in row.iter().enumerate() {
            if value == Some(0) {
                trailheads.push((x, y));
            }
        }
    }

    trailheads
}

fn is_valid_move(topomap: &Topomap, current_height: u32, next_pos: (usize, usize)) -> bool {
    let (x, y) = next_pos;
    let max_y = topomap.len();
    let max_x = topomap[0].len();

    x < max_x && y < max_y && topomap[y][x] == Some(current_height + 1)
}

fn count_reachable_nines(topomap: &Topomap, trailhead: (usize, usize)) -> usize {
    let directions = [(1, 0), (0, 1), (-1, 0), (0, -1)];
    let mut queue = VecDeque::new();
    let mut visited = HashSet::new();
    let mut reachable_nines = 0;

    queue.push_back(trailhead);

    while let Some(current_pos) = queue.pop_front() {
        if !visited.insert(current_pos) {
            continue;
        }

        let (x, y) = current_pos;
        let current_height = topomap[y][x].unwrap();

        if current_height == 9 {
            reachable_nines += 1;
            continue;
        }

        for &(dx, dy) in &directions {
            let next_pos = (x as isize + dx, y as isize + dy);
            if next_pos.0 >= 0 && next_pos.1 >= 0 {
                let next_pos = (next_pos.0 as usize, next_pos.1 as usize);
                if is_valid_move(topomap, current_height, next_pos) {
                    queue.push_back(next_pos);
                }
            }
        }
    }

    reachable_nines
}

fn count_unique_trails(topomap: &Topomap, trailhead: (usize, usize)) -> usize {
    let directions = [(1, 0), (0, 1), (-1, 0), (0, -1)];
    let mut queue = VecDeque::new();
    let mut visited = HashSet::new();
    let mut trail_count = 0;

    queue.push_back((trailhead, vec![trailhead]));

    while let Some((current_pos, mut path)) = queue.pop_front() {
        if !visited.insert(path.clone()) {
            continue;
        }

        let (x, y) = current_pos;
        let current_height = topomap[y][x].unwrap();

        if current_height == 9 {
            trail_count += 1;
            continue;
        }

        for &(dx, dy) in &directions {
            let next_pos = (x as isize + dx, y as isize + dy);
            if next_pos.0 >= 0 && next_pos.1 >= 0 {
                let next_pos = (next_pos.0 as usize, next_pos.1 as usize);
                if is_valid_move(topomap, current_height, next_pos) {
                    path.push(next_pos);
                    queue.push_back((next_pos, path.clone()));
                }
            }
        }
    }

    trail_count
}

fn part1() {
    let input_text = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let topomap = parse_map(&input_text.trim());
    let trailheads = find_trailheads(&topomap);

    let total_score: usize = trailheads
        .into_iter()
        .map(|trailhead| count_reachable_nines(&topomap, trailhead))
        .sum();

    println!("Answer: {}", total_score);
}

fn part2() {
    let input_text = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let topomap = parse_map(&input_text.trim());
    let trailheads = find_trailheads(&topomap);

    let total_rating: usize = trailheads
        .into_iter()
        .map(|trailhead| count_unique_trails(&topomap, trailhead))
        .sum();

    println!("Answer: {}", total_rating);
}

fn main() {
    part1();
    part2();
}
