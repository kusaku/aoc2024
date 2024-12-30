use itertools::Itertools;
use phf::phf_map;
use std::collections::HashMap;
use std::fs;

type Sequence = Vec<char>;

type Moves = HashMap<(char, char), Vec<Sequence>>;

static NUM_KEYPAD: phf::Map<char, (i32, i32)> = phf_map! {
    '7' => (0, 0), '8' => (0, 1), '9' => (0, 2),
    '4' => (1, 0), '5' => (1, 1), '6' => (1, 2),
    '1' => (2, 0), '2' => (2, 1), '3' => (2, 2),
    '#' => (3, 0), '0' => (3, 1), 'A' => (3, 2)
};

static DIR_KEYPAD: phf::Map<char, (i32, i32)> = phf_map! {
    '#' => (0, 0), '^' => (0, 1), 'A' => (0, 2),
    '<' => (1, 0), 'v' => (1, 1), '>' => (1, 2)
};

fn gen_moves(keypad: &phf::Map<char, (i32, i32)>) -> Moves {
    let gap = keypad[&'#'];
    let mut moves = HashMap::new();

    for (&src, &dst) in keypad.keys().cartesian_product(keypad.keys()) {
        if src == '#' || dst == '#' {
            continue;
        }

        let sp = keypad[&src];
        let dp = keypad[&dst];
        let dr = dp.0 - sp.0;
        let dc = dp.1 - sp.1;

        let all_moves: Sequence = [
            vec!['v'; dr.max(0) as usize],
            vec!['^'; (-dr).max(0) as usize],
            vec!['>'; dc.max(0) as usize],
            vec!['<'; (-dc).max(0) as usize],
        ]
        .concat();

        let mut valid = Vec::new();
        for perm in all_moves.iter().permutations(all_moves.len()).unique() {
            let mut pos = sp;

            if perm.iter().all(|&mv| {
                match mv {
                    'v' => pos.0 += 1,
                    '^' => pos.0 -= 1,
                    '>' => pos.1 += 1,
                    '<' => pos.1 -= 1,
                    _ => todo!(),
                }
                pos != gap
            }) {
                let mut seq: Sequence = perm.into_iter().copied().collect();
                seq.push('A');
                valid.push(seq);
            }
        }

        moves.insert((src, dst), valid);
    }

    moves
}

fn min_moves(code: &Sequence, depth: usize, num_moves: &Moves, dir_moves: &Moves) -> usize {
    fn recurse(
        seq: &Sequence,
        d: usize,
        depth: usize,
        num_moves: &Moves,
        dir_moves: &Moves,
        memo: &mut HashMap<(Sequence, usize), usize>,
    ) -> usize {
        if let Some(&res) = memo.get(&(seq.clone(), d)) {
            return res;
        }

        let moves = if d == 0 { num_moves } else { dir_moves };
        let multy_seqs = std::iter::once('A')
            .chain(seq.iter().copied())
            .tuple_windows()
            .map(|(a, b)| &moves[&(a, b)])
            .multi_cartesian_product();

        let mut res = usize::MAX;

        if d == depth {
            for seq_group in multy_seqs {
                let mut seq_cost = 0;
                for seq in seq_group {
                    seq_cost += seq.len();
                }
                res = res.min(seq_cost);
            }
        } else {
            for seq_group in multy_seqs {
                let mut total_cost = 0;
                for step in seq_group {
                    total_cost += recurse(step, d + 1, depth, num_moves, dir_moves, memo);
                }
                res = res.min(total_cost);
            }
        }

        memo.insert((seq.clone(), d), res);
        res
    }

    recurse(code, 0, depth, num_moves, dir_moves, &mut HashMap::new())
}

fn part1() {
    let date = fs::read_to_string("my_input.txt").expect("Failed to read file");
    let codes: Vec<&str> = date.trim().lines().collect();

    let num_moves = gen_moves(&NUM_KEYPAD);
    let dir_moves = gen_moves(&DIR_KEYPAD);

    let total: usize = codes
        .iter()
        .map(|code| {
            let seq: Sequence = code.chars().collect();
            let min_moves_cost = min_moves(&seq, 2, &num_moves, &dir_moves);
            let numeric_part: usize = code[..code.len() - 1].parse().unwrap();
            min_moves_cost * numeric_part
        })
        .sum();

    println!("Answer: {}", total);
}

fn part2() {
    let date = fs::read_to_string("my_input.txt").expect("Failed to read file");
    let codes: Vec<&str> = date.trim().lines().collect();

    let num_moves = gen_moves(&NUM_KEYPAD);
    let dir_moves = gen_moves(&DIR_KEYPAD);

    let total: usize = codes
        .iter()
        .map(|code| {
            let seq: Sequence = code.chars().collect();
            let min_moves_cost = min_moves(&seq, 25, &num_moves, &dir_moves);
            let numeric_part: usize = code[..code.len() - 1].parse().unwrap();
            min_moves_cost * numeric_part
        })
        .sum();

    println!("Answer: {}", total);
}

fn main() {
    part1();
    part2();
}
