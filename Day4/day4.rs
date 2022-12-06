use std::cmp;
use std::env;
use std::fs::File;
use std::io::Read;

fn load_file(file_name: &str) -> String {
    let mut file = File::open(file_name).expect("File not found.");
    let mut data = String::new();
    file.read_to_string(&mut data).expect("File not found.");
    return data.trim_end().to_string();
}

fn get_file_name_arg() -> String {
    let input_args: Vec<String> = env::args().collect();
    let mut file_name: String = "input.txt".to_string();
    if input_args.len() > 1 {
        file_name = input_args[1].clone();
    }
    return file_name;
}

fn parse_interval_extremes(input_line: &str) -> Vec<i32> {
    return input_line
        .split(|c| c == ',' || c == '-')
        .map(|element| element.parse::<i32>().unwrap())
        .collect();
}

fn intervals_contained(intervals: Vec<i32>) -> bool {
    return (intervals[0] - intervals[2]) * (intervals[1] - intervals[3]) <= 0;
}

fn intervals_overlap(intervals: Vec<i32>) -> bool {
    return cmp::max(intervals[0], intervals[2]) <= cmp::min(intervals[1], intervals[3]);
}

fn main() {
    let file_name = get_file_name_arg();
    let data = load_file(&file_name);
    let interal_extremes = data.split("\n").map(|item| parse_interval_extremes(item));
    let result_1 = interal_extremes
        .clone()
        .map(|vector| intervals_contained(vector))
        .into_iter()
        .filter(|b| *b)
        .count();
    let result_2 = interal_extremes
        .map(|vector| intervals_overlap(vector))
        .into_iter()
        .filter(|b| *b)
        .count();
    println!("The number of contained intervals is {}", result_1);
    println!("The number of overlaping intervals is {}", result_2);
}
