use num::BigInt;
use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::fs;
use std::io::{self, Write};
use std::str::FromStr;

static ZERO: Lazy<BigInt> = Lazy::new(|| BigInt::from(0));
static ONE: Lazy<BigInt> = Lazy::new(|| BigInt::from(1));
static MULTIPLIER: Lazy<BigInt> = Lazy::new(|| BigInt::from(2024));

fn blink(stone_counts: &HashMap<BigInt, BigInt>) -> HashMap<BigInt, BigInt> {
    let mut updated_counts = HashMap::new();

    for (stone, count) in stone_counts {
        let stone_str = stone.to_string();
        let stone_str_len = stone_str.len();
        let result = match stone {
            _ if *stone == *ZERO => vec![ONE.clone()],
            _ if stone_str_len % 2 == 0 => {
                let mid = stone_str_len / 2;
                vec![
                    BigInt::from_str(&stone_str[..mid]).unwrap(),
                    BigInt::from_str(&stone_str[mid..]).unwrap(),
                ]
            }
            _ => vec![stone * MULTIPLIER.clone()],
        };

        for new_stone in result {
            *updated_counts.entry(new_stone).or_insert_with(|| ZERO.clone()) += count;
        }
    }

    updated_counts
}

fn count_stones(initial: Vec<BigInt>, blinks: usize) -> BigInt {
    let mut stone_counts: HashMap<BigInt, BigInt> = HashMap::new();
    for stone in initial {
        *stone_counts.entry(stone).or_insert_with(|| ZERO.clone()) += ONE.clone();
    }

    for i in 0..blinks {
        stone_counts = blink(&stone_counts);
        print!("\rProgress: {}%", i * 100 / blinks);
        io::stdout().flush().unwrap();
    }

    println!("\r\x1b[2K");

    stone_counts.values().sum()
}

fn part1() {
    let input_data = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let initial = input_data
        .trim()
        .split_whitespace()
        .map(|s| BigInt::from_str(s).unwrap())
        .collect();

    let result = count_stones(initial, 25);

    println!("Answer: {}", result);
}

fn part2() {
    let input_data = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let initial = input_data
        .trim()
        .split_whitespace()
        .map(|s| BigInt::from_str(s).unwrap())
        .collect();

    let result = count_stones(initial, 75);

    println!("Answer: {}", result);
}

fn part3() {
    let input_data = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let initial = input_data
        .trim()
        .split_whitespace()
        .map(|s| BigInt::from_str(s).unwrap())
        .collect();

    let result = count_stones(initial, 1000);

    println!("Answer: {}", result);
}

fn main() {
    part1();
    part2();
    part3();
}