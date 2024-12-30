use std::collections::{HashMap, HashSet, VecDeque};
use std::fs;
use std::io::{self, Write};
use std::sync::LazyLock;

const DIRECTIONS: &[(char, (isize, isize))] =
    &[('^', (-1, 0)), ('v', (1, 0)), ('<', (0, -1)), ('>', (0, 1))];

static TRANSLATE: LazyLock<HashMap<char, &'static str>> = LazyLock::new(|| {
    HashMap::from([
        ('#', "##"),
        ('O', "[]"),
        ('.', ".."),
        ('@', "@."),
    ])
});

fn parse_input(
    filename: &str,
    is_wide: bool,
) -> (
    Vec<Vec<char>>,
    (usize, usize),
    HashSet<Vec<(usize, usize)>>,
    String,
) {
    let data = fs::read_to_string(filename).expect("Failed to read file");
    let mut layout = Vec::new();
    let mut moves = String::new();
    let mut robot_pos = None;
    let mut boxes = HashSet::new();

    for line in data.trim().lines() {
        if line.starts_with('#') {
            let translated: Vec<char> = if is_wide {
                line.chars()
                    .flat_map(|c| {
                        TRANSLATE
                            .get(&c)
                            .map(|&v| v.to_string()) // Map to `String`
                            .unwrap_or_else(|| c.to_string()) // Use fallback as `String`
                            .chars()
                            .collect::<Vec<_>>()
                    })
                    .collect()
            } else {
                line.chars().collect()
            };
            layout.push(translated);
        } else if DIRECTIONS.iter().any(|(d, _)| line.starts_with(*d)) {
            moves.push_str(line.trim());
        }
    }

    for (r, row) in layout.iter().enumerate() {
        for (c, &char) in row.iter().enumerate() {
            match char {
                '@' => { robot_pos = Some((r, c)); }
                'O' => { boxes.insert(vec![(r, c)]); }
                '[' => { boxes.insert(vec![(r, c), (r, c + 1)]); }
                _ => {}
            }
        }
    }

    (layout, robot_pos.unwrap(), boxes, moves)
}

fn move_robot(
    layout: &[Vec<char>],
    boxes: &mut HashSet<Vec<(usize, usize)>>,
    r: usize,
    c: usize,
    dr: isize,
    dc: isize,
) -> (usize, usize) {
    let rows = layout.len();
    let cols = layout[0].len();
    let target_r = (r as isize + dr) as usize;
    let target_c = (c as isize + dc) as usize;

    if target_r >= rows || target_c >= cols || layout[target_r][target_c] == '#' {
        return (r, c);
    }

    let mut queue = VecDeque::from([(target_r, target_c)]);
    let mut moved = HashSet::new();

    while let Some((curr_r, curr_c)) = queue.pop_front() {
        let current_boxes: Vec<_> = boxes
            .iter()
            .filter(|box_vec| box_vec.contains(&(curr_r, curr_c)) && !moved.contains(*box_vec))
            .cloned()
            .collect();

        for box_vec in current_boxes {
            let mut new_positions = Vec::new();
            for &(br, bc) in &box_vec {
                let nr = (br as isize + dr) as usize;
                let nc = (bc as isize + dc) as usize;
                if nr >= rows || nc >= cols || layout[nr][nc] == '#' {
                    return (r, c);
                }
                new_positions.push((nr, nc));
            }
            queue.extend(&new_positions);
            moved.insert(box_vec.clone());
        }
    }

    boxes.retain(|b| !moved.contains(b));
    boxes.extend(moved.into_iter().map(|b| {
        b.into_iter()
            .map(|(br, bc)| ((br as isize + dr) as usize, (bc as isize + dc) as usize))
            .collect()
    }));

    (target_r, target_c)
}

fn execute(
    layout: &[Vec<char>],
    mut robot_pos: (usize, usize),
    boxes: &mut HashSet<Vec<(usize, usize)>>,
    moves: &str,
) -> (usize, usize) {
    let len = moves.len();
    for (i, move_dir) in moves.chars().enumerate() {
        if i % (len / 100).max(1) == 0 {
            print!("\rProgress: {}%", i * 100 / len);
            io::stdout().flush().unwrap();
        }

        let (dr, dc) = DIRECTIONS.iter().find(|&&(d, _)| d == move_dir).unwrap().1;
        robot_pos = move_robot(layout, boxes, robot_pos.0, robot_pos.1, dr, dc);
    }

    print!("\r\x1b[2K");

    robot_pos
}

fn calculate_gps(boxes: &HashSet<Vec<(usize, usize)>>) -> usize {
    boxes
        .iter()
        .map(|box_vec| {
            let min_r = box_vec.iter().map(|&(r, _)| r).min().unwrap();
            let min_c = box_vec.iter().map(|&(_, c)| c).min().unwrap();
            100 * min_r + min_c
        })
        .sum()
}

fn part1() {
    let (layout, robot_pos, mut boxes, moves) = parse_input("my_input.txt", false);
    let _final_robot_pos = execute(&layout, robot_pos, &mut boxes, &moves);
    let gps_sum = calculate_gps(&boxes);

    println!("Answer: {}", gps_sum);
}

fn part2() {
    let (layout, robot_pos, mut boxes, moves) = parse_input("my_input.txt", true);
    let _final_robot_pos = execute(&layout, robot_pos, &mut boxes, &moves);
    let gps_sum = calculate_gps(&boxes);

    println!("Answer: {}", gps_sum);
}

fn main() {
    part1();
    part2();
}
