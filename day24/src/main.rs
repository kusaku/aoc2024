use itertools::Itertools;
use std::collections::{HashMap, HashSet};
use std::fs;

type Values<'a> = HashMap<&'a str, u8>;
type Gates<'a> = HashSet<(&'a str, &'a str, &'a str, &'a str)>;

fn parse_input(input_text: &str) -> (Values, Gates) {
    let sections: Vec<&str> = input_text.trim().split("\n\n").collect();
    let section_inputs = sections[0];
    let section_gates = sections[1];

    let mut values = HashMap::new();
    for line in section_inputs.lines() {
        let parts: Vec<&str> = line.split(": ").collect();
        let key = parts[0];
        let value: u8 = parts[1].parse().unwrap();
        values.insert(key, value);
    }

    let mut gates = HashSet::new();
    for line in section_gates.lines() {
        let parts: Vec<&str> = line.split(" -> ").collect();
        let out = parts[1];
        for op in [" AND ", " OR ", " XOR "].iter() {
            if parts[0].contains(op) {
                let ins: Vec<&str> = parts[0].split(op).collect();
                let in1 = ins[0];
                let in2 = ins[1];
                gates.insert((op.trim(), in1, in2, out));
                break;
            }
        }
    }

    (values, gates)
}

fn simulate<'a>(values: &mut Values<'a>, gates: &Gates<'a>) {
    let mut remaining_gates = gates.clone();
    while !remaining_gates.is_empty() {
        let ready_gates: HashSet<_> = remaining_gates
            .iter()
            .filter(|gate| values.contains_key(gate.1) && values.contains_key(gate.2))
            .cloned()
            .collect();

        for gate in ready_gates {
            let val1 = values[gate.1];
            let val2 = values[gate.2];

            let result = match gate.0 {
                "AND" => val1 & val2,
                "OR" => val1 | val2,
                "XOR" => val1 ^ val2,
                _ => unreachable!(),
            };

            values.insert(gate.3, result);
            remaining_gates.remove(&gate);
        }
    }
}

fn part1() {
    let input_text = fs::read_to_string("my_input.txt").unwrap();
    let (mut values, gates) = parse_input(&input_text);
    simulate(&mut values, &gates);

    let binary_number: String = values
        .iter()
        .filter(|(key, _)| key.starts_with('z'))
        .collect::<Vec<_>>()
        .into_iter()
        .sorted()
        .rev()
        .map(|(_, bit)| bit.to_string())
        .collect();

    let answer = usize::from_str_radix(&binary_number, 2).unwrap();
    println!("Answer: {}", answer);
}

fn part2() {
    let input_text = fs::read_to_string("my_input.txt").unwrap();
    let (_, gates) = parse_input(&input_text);

    let out = |s_op: &str, s_in: &str| -> Option<&str> {
        for gate in &gates {
            if gate.0 == s_op && (s_in == gate.1 || s_in == gate.2) {
                return Some(gate.3);
            }
        }
        None
    };

    let ins = |s_out: &str| -> HashSet<&str> {
        for gate in &gates {
            if gate.3 == s_out {
                return HashSet::from([gate.1, gate.2]);
            }
        }
        HashSet::new()
    };

    let max_bits = gates
        .iter()
        .filter_map(|gate| gate.3.strip_prefix('z')?.parse::<usize>().ok())
        .max()
        .unwrap_or(0);

    let mut swapped_outs = Vec::new();
    let mut carry_out = out("AND", "x00").unwrap();

    for bit_index in 1..max_bits {
        let input = format!("x{:02}", bit_index);
        let output = format!("z{:02}", bit_index);
        let part_out = out("XOR", &input).unwrap();
        let sum_out = out("XOR", &part_out).or_else(|| out("XOR", &carry_out)).unwrap();
        let full_out = out("AND", &input).unwrap();
        let prop_out = out("AND", &part_out).or_else(|| out("AND", &carry_out)).unwrap();
        let prev_sum_ins = &ins(&sum_out) | &ins(&prop_out);
        if !prev_sum_ins.contains(carry_out) {
            swapped_outs.push(carry_out);
        }
        let sum_out_ins = ins(&sum_out);
        let expected_sum_out = HashSet::from([output.as_str()]);
        carry_out = out("OR", &full_out).or_else(|| out("OR", &prop_out)).unwrap();
        let carry_out_ins = ins(&carry_out);

        if !sum_out_ins.contains(part_out) {
            swapped_outs.push(part_out);
        }
        if !expected_sum_out.contains(sum_out) {
            swapped_outs.push(sum_out);
        }
        if !carry_out_ins.contains(full_out) {
            swapped_outs.push(full_out);
        }
        if !carry_out_ins.contains(prop_out) {
            swapped_outs.push(prop_out);
        }
    }

    println!(
        "Answer: {}",
        swapped_outs
            .into_iter()
            .sorted()
            .collect::<Vec<_>>()
            .join(",")
    );
}

fn main() {
    part1();
    part2();
}