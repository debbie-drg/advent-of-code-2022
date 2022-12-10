use std::collections::HashMap;
use std::collections::HashSet;

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

fn add_to_vector(vector_1: &mut Vec<i32>, vector_2: &Vec<i32>) {
    vector_1[0] += vector_2[0];
    vector_1[1] += vector_2[1];
}

fn vector_difference(vector_1: &Vec<i32>, vector_2: &Vec<i32>) -> Vec<i32> {
    let mut vector_diff = vector_1.clone();
    vector_diff[0] -= vector_2[0];
    vector_diff[1] -= vector_2[1];
    return vector_diff
}

fn grid_distance(head: &Vec<i32>, tail: &Vec<i32>) -> i32 {
    return vector_difference(head, tail)
        .iter()
        .map(|element| element.abs())
        .max()
        .unwrap();
}

fn make_ones(position: Vec<i32>) -> Vec<i32> {
    let mut ones_vector = vec![];
    if position[0] != 0 {
        ones_vector.push(position[0] / position[0].abs());
    } else {
        ones_vector.push(0)
    }
    if position[1] != 0 {
        ones_vector.push(position[1] / position[1].abs());
    } else {
        ones_vector.push(0)
    }
    ones_vector
}

fn move_step(
    rope: &mut Vec<Vec<i32>>,
    command: Vec<&str>,
    positions_visited: &mut HashSet<Vec<i32>>,
    move_correspondence: &HashMap<&str, Vec<i32>>,
) {
    let move_kind = command[0];
    let move_amount = command[1].parse::<usize>().unwrap();
    for _ in 0..move_amount {
        add_to_vector(&mut rope[0], &move_correspondence[move_kind]);
        for index in 1..rope.len() {
            if grid_distance(&rope[index - 1], &rope[index]) <= 1 {
                break;
            }
            let ones_vector = make_ones(vector_difference(&rope[index - 1], &rope[index]));
            add_to_vector(&mut rope[index], &ones_vector);
        }
        positions_visited.insert(rope[rope.len() - 1].clone());
    }
}

fn move_all(
    commands: &Vec<&str>,
    rope_length: usize,
    move_correspondence: &HashMap<&str, Vec<i32>>,
) -> HashSet<Vec<i32>> {
    let mut rope = vec![vec![0, 0]; rope_length];
    let mut positions_visited: HashSet<Vec<i32>> = HashSet::new();
    for command in commands {
        let current_command = command.split(" ").collect();
        move_step(
            &mut rope,
            current_command,
            &mut positions_visited,
            &move_correspondence,
        );
    }
    return positions_visited;
}

fn main() {
    let data = get_data();
    let split_data = data.split("\n").collect();
    let move_correspondence: HashMap<&str, Vec<i32>> = HashMap::from([
        ("R", vec![1, 0]),
        ("L", vec![-1, 0]),
        ("U", vec![0, 1]),
        ("D", vec![0, -1]),
    ]);
    let visited_part_1 = move_all(&split_data, 2, &move_correspondence);
    println!(
        "The number of points visited for size 2 is {}.",
        visited_part_1.len()
    );

    let visited_part_2 = move_all(&split_data, 10, &move_correspondence);
    println!(
        "The number of points visited for size 10 is {}.",
        visited_part_2.len()
    )
}
