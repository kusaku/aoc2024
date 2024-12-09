use std::fs;
use std::io::{self, Write};

const EMPTY_SPACE: usize = usize::MAX;

type Block = (usize, usize); // (file identifier or EMPTY_SPACE, length)

fn defragment(blocks: &mut Vec<Block>, move_whole_files: bool) {
    let mut total_blocks = blocks.len();
    let mut last_progress = 0;
    let mut search_span_from = 0;

    for i in (0..total_blocks).rev() {
        let progress = (total_blocks - i) * 100 / total_blocks;

        if progress != last_progress {
            print!("\rProgress: {}%", progress);
            io::stdout().flush().unwrap();
            last_progress = progress;
        }

        let (file_id, file_length) = blocks[i];
        if file_id != EMPTY_SPACE {
            for k in search_span_from..i {
                let (span_id, span_length) = blocks[k];

                if span_id == EMPTY_SPACE && span_length >= file_length {
                    blocks[k] = (file_id, file_length);
                    blocks[i] = (span_id, file_length);

                    if span_length > file_length {
                        blocks.insert(k + 1, (span_id, span_length - file_length));
                        total_blocks += 1;
                    }

                    if !move_whole_files {
                        search_span_from = k;
                    }

                    break;
                }
            }
        }
    }

    print!("\r\033[2K\r");
}

fn calculate_checksum(blocks: &[Block]) -> usize {
    let mut checksum = 0;
    let mut position = 0;

    for &(block_id, block_length) in blocks {
        if block_id != EMPTY_SPACE {
            for pos in position..position + block_length {
                checksum += pos * block_id;
            }
        }
        position += block_length;
    }

    checksum
}

fn part1() {
    let disk_map = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let mut blocks: Vec<Block> = disk_map
        .trim()
        .to_string()
        .chars()
        .enumerate()
        .flat_map(|(i, char)| {
            let count = char.to_digit(10).unwrap() as usize;
            (0..count).map(move |_| {
                if i % 2 == 0 {
                    (i / 2, 1)
                } else {
                    (EMPTY_SPACE, 1)
                }
            })
        })
        .collect();

    defragment(&mut blocks, false);
    let result = calculate_checksum(&blocks);
    println!("Answer: {}", result);
}

fn part2() {
    let disk_map = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let mut blocks: Vec<Block> = disk_map
        .trim()
        .to_string()
        .chars()
        .enumerate()
        .map(|(i, char)| {
            let count = char.to_digit(10).unwrap() as usize;
            if i % 2 == 0 {
                (i / 2, count)
            } else {
                (EMPTY_SPACE, count)
            }
        })
        .collect();

    defragment(&mut blocks, true);
    let result = calculate_checksum(&blocks);
    println!("Answer: {}", result);
}

fn main() {
    part1();
    part2();
}
