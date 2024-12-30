use regex::Regex;
use std::fs;

fn part1() {
    let memory = fs::read_to_string("my_input.txt").expect("Failed to read file");
    let pattern = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
    let total_sum: i32 = pattern
        .captures_iter(memory.trim())
        .map(|cap| {
            let x: i32 = cap[1].parse().unwrap();
            let y: i32 = cap[2].parse().unwrap();
            x * y
        })
        .sum();
    println!("Answer: {}", total_sum);
}

fn part2() {
    let memory = fs::read_to_string("my_input.txt").expect("Failed to read file");
    let pattern = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\)|don't\(\))").unwrap();
    let mut mul_enabled = true;
    let mut total_sum = 0;

    for cap in pattern.captures_iter(memory.trim()) {
        if mul_enabled {
            if let (Some(x), Some(y)) = (cap.get(1), cap.get(2)) {
                let x: i32 = x.as_str().parse().unwrap();
                let y: i32 = y.as_str().parse().unwrap();
                total_sum += x * y;
            }
        }
        if let Some(control) = cap.get(3) {
            mul_enabled = control.as_str() == "do()";
        }
    }

    println!("Answer: {}", total_sum);
}

fn main() {
    part1();
    part2();
}
