use std::fs::read_to_string;
use std::io::{self, Write};

fn read_input(file_path: &str) -> Vec<(i64, Vec<i64>)> {
    let input_data = read_to_string(file_path).expect("Failed to read input file");
    input_data
        .lines()
        .map(|line| {
            let parts: Vec<&str> = line.split(':').collect();
            let test_value = parts[0].trim().parse::<i64>().expect("Invalid test value");
            let numbers = parts[1]
                .trim()
                .split_whitespace()
                .map(|n| n.parse::<i64>().expect("Invalid number"))
                .collect();
            (test_value, numbers)
        })
        .collect()
}

fn evaluate_expression(numbers: &[i64], operators: &[&str]) -> i64 {
    let mut result = numbers[0];
    for (i, &op) in operators.iter().enumerate() {
        match op {
            "+" => result += numbers[i + 1],
            "*" => result *= numbers[i + 1],
            "||" => {
                result = format!("{}{}", result, numbers[i + 1])
                    .parse::<i64>()
                    .unwrap()
            }
            _ => panic!("Unknown operator"),
        }
    }
    result
}

fn is_valid_equation(test_value: i64, numbers: &[i64], allowed_operators: &[&str]) -> bool {
    let n = numbers.len() - 1;
    let k = allowed_operators.len();

    for mut i in 0..k.pow(n as u32) {
        let mut operators = Vec::with_capacity(n);

        for _ in 0..n {
            operators.push(allowed_operators[i % k]);
            i /= k;
        }

        if evaluate_expression(numbers, &operators) == test_value {
            return true;
        }
    }

    false
}

fn calculate_total_calibration(file_path: &str, allowed_operators: &[&str]) -> i64 {
    let equations = read_input(file_path);
    let total_equations = equations.len();
    let mut total_calibration_result = 0;
    let mut completed = 0;
    let mut last_percent = 0;

    for (test_value, numbers) in equations {
        if is_valid_equation(test_value, &numbers, allowed_operators) {
            total_calibration_result += test_value;
        }
        completed += 1;
        let percent = completed * 100 / total_equations;
        if percent > last_percent {
            print!("\rProgress: {}%", percent);
            io::stdout().flush().unwrap();
            last_percent = percent;
        }
    }

    print!("\r\033[2K\r");

    total_calibration_result
}

fn part1() {
    let result = calculate_total_calibration("my_input.txt", &["+", "*"]);
    println!("Answer: {}", result);
}

fn part2() {
    let result = calculate_total_calibration("my_input.txt", &["+", "*", "||"]);
    println!("Answer: {}", result);
}

fn main() {
    part1();
    part2();
}
