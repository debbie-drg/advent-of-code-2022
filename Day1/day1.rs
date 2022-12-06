use std::env;
use std::fs::File;
use std::io::Read;

fn load_file_split_strings(file_name: &str) -> String {
    let mut file = File::open(file_name).expect("File not found.");
    let mut data = String::new();
    file.read_to_string(&mut data).expect("File not found.");
    return data;
}

fn get_file_name_arg() -> String {
    let input_args: Vec<String> = env::args().collect();
    let mut file_name: String = "input.txt".to_string();
    if input_args.len() > 1 {
        file_name = input_args[1].clone();
    }
    return file_name;
}

fn main() {
    let file_name = get_file_name_arg();
    let data = load_file_split_strings(&file_name);
    let mut calories: Vec<_> = data
        .split("\n\n")
        .map(|element| {
            element
                .lines()
                .map(|item| item.parse::<u32>().unwrap())
                .sum::<u32>()
        })
        .collect();
    calories.sort();
    calories.reverse();
    println!("Top: {}", calories[0]);
    let biggest_three = calories[0..3].iter().sum::<u32>();
    println!("Top three: {}", biggest_three)
}
