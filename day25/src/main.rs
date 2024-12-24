use std::fs;

fn part1() {
    let data = fs::read_to_string("my_input.txt").expect("Failed to read file");
    let mut locks = Vec::new();
    let mut keys = Vec::new();

    for schematic in data.trim().split("\n\n") {
        let rows: Vec<&str> = schematic.lines().collect();
        let heights: Vec<usize> = (0..rows[0].len())
            .map(|col| rows.iter().filter(|row| row.chars().nth(col) == Some('#')).count() - 1)
            .collect();

        if rows[0].chars().all(|c| c == '#') { locks.push(heights) } else { keys.push(heights) }
    }

    let fitting_pairs_count: usize = locks
        .iter()
        .map(|lock| {
            keys.iter()
                .filter(|key| lock.iter().zip(key.iter()).all(|(l, k)| l + k <= 5))
                .count()
        })
        .sum();

    println!("Answer: {}", fitting_pairs_count);
}

fn main() {
    part1();
}
