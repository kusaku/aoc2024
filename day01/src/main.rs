use std::collections::HashMap;
use std::fs;

fn parse_input(filename: &str) -> (Vec<i32>, Vec<i32>) {
    fs::read_to_string(filename)
        .expect("Failed to read file")
        .trim()
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|n| n.parse().unwrap())
                .collect::<Vec<i32>>()
        })
        .map(|nums| (nums[0], nums[1]))
        .unzip()
}

fn part1() {
    let total_distance: i32 = {
        let (mut left_list, mut right_list) = parse_input("my_input.txt");
        left_list.sort();
        right_list.sort();
        left_list
            .iter()
            .zip(right_list.iter())
            .map(|(l, r)| (l - r).abs())
            .sum()
    };

    println!("Answer: {}", total_distance);
}

fn part2() {
    let similarity_score: i32 = {
        let (left_list, right_list) = parse_input("my_input.txt");
        let right_count = right_list.into_iter().fold(HashMap::new(), |mut acc, num| {
            *acc.entry(num).or_insert(0) += 1;
            acc
        });
        left_list
            .iter()
            .map(|num| num * right_count.get(num).unwrap_or(&0))
            .sum()
    };

    println!("Answer: {}", similarity_score);
}

fn main() {
    part1();
    part2();
}
