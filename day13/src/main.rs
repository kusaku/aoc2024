use std::fs;

fn parse_machine(file_name: &str) -> Vec<(i64, i64, i64, i64, i64, i64)> {
    fs::read_to_string(file_name)
        .expect("Unable to read file")
        .trim()
        .split("\n\n")
        .map(|block| {
            let lines: Vec<&str> = block.split('\n').collect();
            let parse_line = |line: &str, x_delim: &str, y_delim: &str| {
                let parts: Vec<i64> = line
                    .split(x_delim).nth(1).unwrap()
                    .split(y_delim).map(|v| v.parse().expect("Invalid number")).collect();
                (parts[0], parts[1])
            };

            let (a1, a2) = parse_line(lines[0], "X+", ", Y+");
            let (b1, b2) = parse_line(lines[1], "X+", ", Y+");
            let (p1, p2) = parse_line(lines[2], "X=", ", Y=");

            (a1, b1, p1, a2, b2, p2)
        })
        .collect()
}

fn solve_system(a1: i64, b1: i64, p1: i64, a2: i64, b2: i64, p2: i64) -> Option<(i64, i64)> {
    let (d, x_num, y_num) = (a1 * b2 - a2 * b1, b2 * p1 - p2 * b1, a1 * p2 - a2 * p1);

    if d == 0 || x_num % d != 0 || y_num % d != 0 {
        None
    } else {
        let (x, y) = (x_num / d, y_num / d);
        (x >= 0 && y >= 0).then_some((x, y))
    }
}

fn part1() {
    let machines = parse_machine("my_input.txt");
    let mut total_cost = 0;

    for (i, &(a1, b1, p1, a2, b2, p2)) in machines.iter().enumerate() {
        if let Some((x, y)) = solve_system(a1, b1, p1, a2, b2, p2) {
            total_cost += x * 3 + y;
        }
        let progress = (i + 1) * 100 / machines.len();
        print!("\rProgress: {}%", progress);
    }

    print!("\r\x1b[2K");
    println!("Answer: {}", total_cost);
}

fn part2() {
    let machines = parse_machine("my_input.txt");
    let mut total_cost = 0;
    let offset = 10_000_000_000_000;

    for (i, &(a1, b1, p1, a2, b2, p2)) in machines.iter().enumerate() {
        if let Some((x, y)) = solve_system(a1, b1, p1 + offset, a2, b2, p2 + offset) {
            total_cost += x * 3 + y;
        }
        let progress = (i + 1) * 100 / machines.len();
        print!("\rProgress: {}%", progress);
    }

    print!("\r\x1b[2K");
    println!("Answer: {}", total_cost);
}

fn main() {
    part1();
    part2();
}
