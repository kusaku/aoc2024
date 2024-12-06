use std::collections::{HashMap, HashSet};
use std::fs;

fn parse_input(file_path: &str) -> (Vec<(usize, usize)>, Vec<Vec<usize>>) {
    let input_text = fs::read_to_string(file_path).unwrap();
    let mut sections = input_text.split("\n\n");
    let rules_section = sections.next().unwrap();
    let updates_section = sections.next().unwrap();

    let rules: Vec<(usize, usize)> = rules_section
        .lines()
        .map(|line| {
            let mut parts = line.split('|').map(|n| n.parse::<usize>().unwrap());
            (parts.next().unwrap(), parts.next().unwrap())
        })
        .collect();

    let updates: Vec<Vec<usize>> = updates_section
        .lines()
        .map(|line| {
            line.split(',')
                .map(|n| n.parse::<usize>().unwrap())
                .collect()
        })
        .collect();

    (rules, updates)
}

fn is_order_correct(update: &[usize], rules: &[(usize, usize)]) -> bool {
    let positions: HashMap<_, _> = update
        .iter()
        .enumerate()
        .map(|(i, &page)| (page, i))
        .collect();

    rules.iter().all(|&(x, y)| {
        positions
            .get(&x)
            .and_then(|&pos_x| positions.get(&y).map(|&pos_y| pos_x < pos_y))
            .unwrap_or(true)
    })
}

fn sort_update(update: &[usize], rules: &[(usize, usize)]) -> Vec<usize> {
    let mut graph: HashMap<usize, HashSet<usize>> =
        update.iter().map(|&page| (page, HashSet::new())).collect();
    let mut indegree: HashMap<usize, usize> = update.iter().map(|&page| (page, 0)).collect();

    for &(x, y) in rules {
        if let (Some(neighbors), Some(deg)) = (graph.get_mut(&x), indegree.get_mut(&y)) {
            neighbors.insert(y);
            *deg += 1;
        }
    }

    let mut stack: Vec<usize> = indegree
        .iter()
        .filter_map(|(&page, &deg)| (deg == 0).then_some(page))
        .collect();

    let mut sorted_update = Vec::with_capacity(update.len());

    while let Some(current) = stack.pop() {
        sorted_update.push(current);

        if let Some(neighbors) = graph.get(&current) {
            for &neighbor in neighbors {
                if let Some(deg) = indegree.get_mut(&neighbor) {
                    *deg -= 1;
                    if *deg == 0 {
                        stack.push(neighbor);
                    }
                }
            }
        }
    }

    sorted_update
}

fn part1() {
    let (rules, updates) = parse_input("my_input.txt");
    let correct_middle_sum: usize = updates
        .iter()
        .filter(|update| is_order_correct(update, &rules))
        .map(|update| update[update.len() / 2])
        .sum();

    println!("Answer: {}", correct_middle_sum);
}

fn part2() {
    let (rules, updates) = parse_input("my_input.txt");
    let incorrect_middle_sum: usize = updates
        .iter()
        .filter(|update| !is_order_correct(update, &rules))
        .map(|update| sort_update(update, &rules))
        .map(|update| update[update.len() / 2])
        .sum();

    println!("Answer: {}", incorrect_middle_sum);
}

fn main() {
    part1();
    part2();
}
