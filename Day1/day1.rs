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

fn main() {
    let data = get_data();
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
