use itertools::Itertools;
use std::collections::{HashMap, HashSet};
use std::fs;

const MASK_24BIT: i64 = 0xFFFFFF;
const GENS: usize = 2000;
const SEQ_LEN: usize = 4;

fn part1() {
    let data = fs::read_to_string("my_input.txt").expect("Failed to read file");
    let secrets: Vec<i64> = data.lines().map(|line| line.parse().unwrap()).collect();

    let mut secret_sum = 0;
    for mut secret in secrets {
        for _ in 0..GENS {
            secret = ((secret << 6) ^ secret) & MASK_24BIT;
            secret = ((secret >> 5) ^ secret) & MASK_24BIT;
            secret = ((secret << 11) ^ secret) & MASK_24BIT;
        }
        secret_sum += secret;
    }

    println!("Answer: {}", secret_sum);
}

fn part2() {
    let data = fs::read_to_string("my_input.txt").expect("Failed to read file");
    let secrets: Vec<i64> = data.lines().map(|line| line.parse().unwrap()).collect();

    let mut amounts: HashMap<Vec<i64>, i64> = HashMap::new();
    for mut secret in secrets {
        let mut digits: Vec<i64> = vec![];
        for _ in 0..GENS {
            secret = ((secret << 6) ^ secret) & MASK_24BIT;
            secret = ((secret >> 5) ^ secret) & MASK_24BIT;
            secret = ((secret << 11) ^ secret) & MASK_24BIT;
            digits.push(secret % 10);
        }
        let deltas: Vec<i64> = digits.iter().tuple_windows().map(|(a, b)| b - a).collect();
        let mut seen_sequences = HashSet::new();
        for (key, &price) in deltas.windows(SEQ_LEN).zip(digits.iter().skip(SEQ_LEN)) {
            if seen_sequences.insert(key) {
                *amounts.entry(key.to_vec()).or_insert(0) += price;
            }
        }
    }

    println!("Answer: {}", amounts.values().max().unwrap());
}

fn main() {
    part1();
    part2();
}
