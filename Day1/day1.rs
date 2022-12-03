use std::fs::File;
use std::io::Read;

fn load_file_split_strings(file_name: &str) -> String {
    let mut file = File::open(file_name).expect("File not found.");
    let mut data = String::new();
    file.read_to_string(&mut data).expect("File not found.");
    return data;
}

fn main() {
    let data = load_file_split_strings("input.txt");
    let mut calories: Vec<_> = data.split("\n\n").map(|element| element.lines().map(|item| item.parse::<i32>().unwrap()).sum::<i32>()).collect();
    calories.sort();
    calories.reverse();
    println!("Top: {}", calories[0]);
    let biggest_three = calories[0..3].iter().sum::<i32>();
    println!("Top three: {}", biggest_three)
}