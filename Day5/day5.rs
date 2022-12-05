use std::fs::File;
use std::io::Read;

fn load_file(file_name: &str) -> String {
    let mut file = File::open(file_name).expect("File not found.");
    let mut data = String::new();
    file.read_to_string(&mut data).expect("File not found.");
    return data.trim_end().to_string();
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
                _ => panic!("unexpected input: {:?}", instruction)
            }
        }
        moves.push((count, source - 1, destination - 1))
    }
    return moves
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
    return stacks
}

fn perform_moves(instructions: &[(usize, usize, usize)], mut stacks: Vec<Vec<char>>, mode_9001: bool) -> Vec<Vec<char>> {
    for (count, source, destination) in instructions.iter().copied() {
        let mut current_vector = vec![];
        for _ in 0..count {
            current_vector.push(stacks[source].pop().unwrap());
        }
        if mode_9001 == true {
            current_vector.reverse();
        }

        stacks[destination].append(&mut current_vector);
        
    }
    return stacks
}

fn get_top_elements(stacks: &Vec<Vec<char>>) -> String {
    let mut answer = String::with_capacity(stacks.len());
    for stack in stacks {
        answer.push(stack.last().unwrap().clone());
    }
    return answer
}

fn main() {
    let data = load_file("input.txt");
    let stacks_and_instructions: Vec<&str> = data.split("\n\n").collect();
    let mut stacks_9000 = extract_stacks(stacks_and_instructions[0]);
    let mut stacks_9001 = stacks_9000.clone();
    let instructions = extract_moves_from_instructions(stacks_and_instructions[1]);

    stacks_9000 = perform_moves(&instructions, stacks_9000, false);
    stacks_9001 = perform_moves(&instructions, stacks_9001, true);

    let answer_part_1 = get_top_elements(&stacks_9000);
    let answer_part_2 = get_top_elements(&stacks_9001);
    
    println!("The elements at the top after moving with CrateMover 9000 are {}", answer_part_1);
    println!("The elements at the top after moving with CrateMover 9001 are {}", answer_part_2);    
}
