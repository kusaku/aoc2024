use std::collections::HashMap;
use std::fs;

fn count_segmentations(string: &str, segments: &[&str]) -> usize {
    let mut memo: HashMap<String, usize> = HashMap::from([(String::new(), 1)]);

    fn inner(string: &str, segments: &[&str], memo: &mut HashMap<String, usize>) -> usize {
        if let Some(&count) = memo.get(string) {
            return count;
        }

        let count = segments
            .iter()
            .filter(|&&segment| string.starts_with(segment))
            .map(|&segment| inner(&string[segment.len()..], segments, memo))
            .sum();

        memo.insert(string.to_string(), count);
        count
    }

    inner(string, segments, &mut memo)
}

fn part1() {
    let input_data = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let parts: Vec<&str> = input_data.trim().split("\n\n").collect();
    let patterns: Vec<&str> = parts[0].split(", ").collect();
    let designs: Vec<&str> = parts[1].split('\n').collect();

    let possible_count = designs
        .iter()
        .filter(|design| count_segmentations(&design, &patterns) > 0)
        .count();

    println!("Answer: {}", possible_count);
}

fn part2() {
    let input_data = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let parts: Vec<&str> = input_data.trim().split("\n\n").collect();
    let patterns: Vec<&str> = parts[0].split(", ").collect();
    let designs: Vec<&str> = parts[1].split('\n').collect();

    let total_ways: usize = designs
        .iter()
        .map(|design| count_segmentations(&design, &patterns))
        .sum();

    println!("Answer: {}", total_ways);
}

fn main() {
    part1();
    part2();
}
