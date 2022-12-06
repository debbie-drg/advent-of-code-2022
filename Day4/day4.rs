use std::cmp;

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
    let data = get_data();
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
