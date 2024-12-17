use std::fs;

fn parse_data(filename: &str) -> ((u64, u64, u64), Vec<u64>) {
    let data = fs::read_to_string(filename).expect("Failed to read input file");
    let lines: Vec<&str> = data.lines().filter(|line| !line.trim().is_empty()).collect();
    let a = lines[0].split(":").nth(1).unwrap().trim().parse::<u64>().unwrap();
    let b = lines[1].split(":").nth(1).unwrap().trim().parse::<u64>().unwrap();
    let c = lines[2].split(":").nth(1).unwrap().trim().parse::<u64>().unwrap();
    let program = lines[3]
        .split(":")
        .nth(1)
        .unwrap()
        .trim()
        .split(',')
        .map(|x| x.parse::<u64>().unwrap())
        .collect();

    ((a, b, c), program)
}

// Function to run the program
fn run_program(registers: (u64, u64, u64), program: &[u64]) -> Vec<u64> {
    let (mut a, mut b, mut c) = registers;
    let mut ip = 0;
    let mut output = Vec::new();

    while ip < program.len() {
        let opcode = program[ip];
        let operand = if ip + 1 < program.len() { program[ip + 1] } else { 0 };

        // Helper function to determine combo operand values
        let combo_value = |operand: u64| -> u64 {
            match operand {
                0..=3 => operand,
                4 => a,
                5 => b,
                6 => c,
                _ => 0,
            }
        };

        match opcode {
            0 => {
                // adv - divide A by 2^(combo operand)
                let denominator = 1 << combo_value(operand);
                a /= denominator;
            }
            1 => {
                // bxl - XOR B with literal operand
                b ^= operand;
            }
            2 => {
                // bst - set B to (combo operand) % 8
                b = combo_value(operand) % 8;
            }
            3 => {
                // jnz - jump to operand if A is non-zero
                if a != 0 {
                    ip = operand as usize;
                    continue;
                }
            }
            4 => {
                // bxc - XOR B with C
                b ^= c;
            }
            5 => {
                // out - output (combo operand) % 8
                output.push(combo_value(operand) % 8);
            }
            6 => {
                // bdv - divide A by 2^(combo operand), result in B
                let denominator = 1 << combo_value(operand);
                b = a / denominator;
            }
            7 => {
                // cdv - divide A by 2^(combo operand), result in C
                let denominator = 1 << combo_value(operand);
                c = a / denominator;
            }
            _ => break,
        }

        ip += 2;
    }

    output
}

fn part1() {
    let (registers, program) = parse_data("my_input.txt");
    let result = run_program(registers, &program);
    let answer = result
        .iter()
        .map(ToString::to_string)
        .collect::<Vec<_>>()
        .join(",");

    println!("Answer: {}", answer);
}

fn part2() {
    let (_, program) = parse_data("my_input.txt");
    let (mut a, b, c) = (1 << (3 * (program.len() - 1)), 0, 0);
    let mut result = vec![0; program.len()];

    while result != program {
        for pos in (0..program.len()).rev() {
            if result[pos] != program[pos] {
                a += 1 << (3 * pos);
                result = run_program((a, b, c), &program);
            }
        }
    }

    println!("Answer: {}", a);
}

fn main() {
    part1();
    part2();
}
