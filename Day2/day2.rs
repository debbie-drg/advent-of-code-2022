use std::collections::HashMap;

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

// We codify the outcomes as follows:
// - 0 for Rock
// - 1 for Paper
// - 2 for Scissors
// Then Draw if equal, Win if index for player 2 is one more than for player 1, Lose otherwise.
// Using this we can easily compute the game result.

fn game_result(player_1: &i32, player_2: &i32) -> i32 {
    return (1 + player_2 - player_1).rem_euclid(3);
}

fn total_points(player_1: &i32, player_2: &i32) -> i32 {
    return player_2 + 1 + 3 * game_result(player_1, player_2);
}

fn player_two_move_round_two(player_1: &i32, player_2: &i32) -> i32 {
    return (player_1 + player_2 - 1).rem_euclid(3);
}

fn compute_hashmaps() -> (HashMap<String, i32>, HashMap<String, i32>) {
    let mut hashmap_1: HashMap<String, i32> = HashMap::new();
    let mut hashmap_2: HashMap<String, i32> = HashMap::new();
    let player_1 = ["A", "B", "C"];
    let player_2 = ["X", "Y", "Z"];
    for index_player_1 in 0..player_1.len() {
        for index_player_2 in 0..player_2.len() {
            let index_1 = index_player_1 as i32;
            let index_2 = index_player_2 as i32;
            let index_strings =
                format!("{} {}", player_1[index_player_1], player_2[index_player_2]).to_string();
            let index_strings_copy = index_strings.clone();
            let result_round_1 = total_points(&index_1, &index_2);
            hashmap_1.insert(index_strings, result_round_1);
            let player_2_round_2 = player_two_move_round_two(&index_1, &index_2);
            let result_round_2 = total_points(&index_1, &player_2_round_2);
            hashmap_2.insert(index_strings_copy, result_round_2);
        }
    }
    return (hashmap_1, hashmap_2);
}

fn main() {
    let data = get_data();
    let (hashmap_round_1, hashmap_round_2) = compute_hashmaps();
    let data_lines = data.split("\n");
    let result_1 = data_lines
        .clone()
        .map(|item| hashmap_round_1[item])
        .sum::<i32>();
    let result_2 = data_lines.map(|item| hashmap_round_2[item]).sum::<i32>();
    println!("The final score for Round 1 is {}", result_1);
    println!("The final score for Round 2 is {}", result_2);
}
