fn get_data() -> String {
    let input_args: Vec<String> = std::env::args().collect();
    let mut file_name: String = "input.txt".to_string();
    if input_args.len() > 1 {
        file_name = input_args[1].clone();
    }
    let mut data = std::fs::read_to_string(file_name).unwrap();
    if data.ends_with("\n") {
        data.pop();
    }
    return data;
}

fn extract_moves_from_instructions(instructions: &str) -> Vec<(usize, usize, usize)> {
    let mut count: usize = 0;
    let mut source: usize = 0;
    let mut destination: usize = 0;

    let mut moves = vec![];

    for instruction in instructions.lines() {
        for (idx, part) in instruction.split(' ').enumerate() {
            match idx {
                0 | 2 | 4 => continue,
                1 => count = part.parse().unwrap(),
                3 => source = part.parse().unwrap(),
                5 => destination = part.parse().unwrap(),
                _ => panic!("unexpected input: {:?}", instruction),
            }
        }
        moves.push((count, source - 1, destination - 1))
    }
    return moves;
}

fn extract_stacks(stacks_input: &str) -> Vec<Vec<char>> {
    let mut stacks = vec![vec![]];

    for line in stacks_input.lines() {
        if !line.starts_with(" 1") {
            for (idx, value) in line.as_bytes().chunks(4).enumerate() {
                if stacks.len() <= idx {
                    stacks.push(vec![]);
                }

                if value[1 as usize] != b' ' as u8 {
                    stacks[idx].push(value[1 as usize] as char);
                }
            }
        }
    }
    // We have the stacks but they are reversed
    for stack in stacks.iter_mut() {
        stack.reverse();
    }
    return stacks;
}

fn perform_moves(
    instructions: &[(usize, usize, usize)],
    mut stacks: Vec<Vec<char>>,
    mode_9001: bool,
) -> Vec<Vec<char>> {
    for (count, source, destination) in instructions.iter().copied() {
        let split_point = stacks[source].len() - count;
        let mut crates_to_move = stacks[source].split_off(split_point);

        if mode_9001 == false {
            crates_to_move.reverse();
        }

        stacks[destination].append(&mut crates_to_move);
    }
    return stacks;
}

fn get_top_elements(stacks: &Vec<Vec<char>>) -> String {
    let mut answer = String::with_capacity(stacks.len());
    for stack in stacks {
        answer.push(stack.last().unwrap().clone());
    }
    return answer;
}

fn main() {
    let data = get_data();
    let stacks_and_instructions: Vec<&str> = data.split("\n\n").collect();
    let mut stacks_9000 = extract_stacks(stacks_and_instructions[0]);
    let mut stacks_9001 = stacks_9000.clone();
    let instructions = extract_moves_from_instructions(stacks_and_instructions[1]);

    stacks_9000 = perform_moves(&instructions, stacks_9000, false);
    stacks_9001 = perform_moves(&instructions, stacks_9001, true);

    let answer_part_1 = get_top_elements(&stacks_9000);
    let answer_part_2 = get_top_elements(&stacks_9001);

    println!(
        "The elements at the top after moving with CrateMover 9000 are {}",
        answer_part_1
    );
    println!(
        "The elements at the top after moving with CrateMover 9001 are {}",
        answer_part_2
    );
}
