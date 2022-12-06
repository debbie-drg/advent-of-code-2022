extern crate array_tool;

use array_tool::vec::Intersect;

const UPPERCASE_DIFF: u32 = 38;
const LOWERCASE_DIFF: u32 = 58;

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

fn score_item(item: &str) -> u32 {
    let scored_item = item.as_bytes()[0] as u32;
    return (scored_item - UPPERCASE_DIFF).rem_euclid(LOWERCASE_DIFF);
}

fn vector_from_string(string_input: &str) -> Vec<&str> {
    return string_input
        .split("")
        .filter(|leter| !leter.is_empty())
        .collect::<Vec<&str>>();
}

fn main() {
    let data = get_data();
    let data_lines = data.split("\n");
    let score_1 = data_lines
        .clone()
        .map(|line| {
            let (half_1, half_2) = line.split_at((line.len() / 2) as usize);
            let vector_1 = vector_from_string(half_1);
            let vector_2 = vector_from_string(half_2);
            return score_item(vector_1.intersect(vector_2)[0]);
        })
        .sum::<u32>();
    let score_2 = data_lines
        .collect::<Vec<&str>>()
        .chunks(3)
        .map(|chunk| {
            let vector_1 = vector_from_string(chunk[0]);
            let vector_2 = vector_from_string(chunk[1]);
            let intersection = vector_1.intersect(vector_2);
            let vector_3 = vector_from_string(chunk[2]);
            return score_item(intersection.intersect(vector_3)[0]);
        })
        .sum::<u32>();
    println!("The score for part one is {} ", score_1);
    println!("The score for part two is {} ", score_2);
}
