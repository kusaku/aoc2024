use std::fs;

fn parse_input() -> Vec<Vec<i32>> {
    fs::read_to_string("my_input.txt")
        .expect("Error reading file")
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|n| n.parse::<i32>().unwrap())
                .collect()
        })
        .collect()
}

fn is_report_safe(report: &Vec<i32>) -> bool {
    let differences: Vec<i32> = report.windows(2).map(|pair| pair[1] - pair[0]).collect();
    let increasing = differences.iter().all(|&diff| (1..=3).contains(&diff));
    let decreasing = differences.iter().all(|&diff| (-3..=-1).contains(&diff));
    increasing || decreasing
}

fn is_report_safe_with_dampener(report: &Vec<i32>) -> bool {
    if is_report_safe(report) {
        return true;
    }
    for i in 0..report.len() {
        let mut modified_report = report.clone();
        modified_report.remove(i);
        if is_report_safe(&modified_report) {
            return true;
        }
    }
    false
}

fn part1() {
    let safe_reports = parse_input()
        .iter()
        .filter(|report| is_report_safe(report))
        .count();
    println!("Answer: {}", safe_reports);
}

fn part2() {
    let safe_reports_with_dampener = parse_input()
        .iter()
        .filter(|report| is_report_safe_with_dampener(report))
        .count();
    println!("Answer: {}", safe_reports_with_dampener);
}

fn main() {
    part1();
    part2();
}
