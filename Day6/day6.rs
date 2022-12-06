use std::env;

fn get_data() -> String {
    let input_args: Vec<String> = env::args().collect();
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

fn detect_first_marker(datastream: &str, length_of_indicator: usize) -> usize {
    return datastream.as_bytes()
        .windows(length_of_indicator)
        .position(|window| {
            window
                .iter()
                .enumerate()
                .all(|(idx, c)| !window[..idx].contains(c))
        })
        .unwrap()
        + length_of_indicator
}

fn main() {
    let data = get_data();
    let data_chunks: Vec<&str> = data.split("\n").collect();
    let start_of_packets: Vec<usize> = data_chunks
        .clone()
        .into_iter()
        .map(|chunk| detect_first_marker(&chunk, 4))
        .collect();
    let start_of_messages: Vec<usize> = data_chunks
        .into_iter()
        .map(|chunk| detect_first_marker(&chunk, 14))
        .collect();
    println!(
        "The first start-of-packet marker for the given message/s at {:?}",
        start_of_packets
    );
    println!(
        "The first start-of-message marker for the given message/s at {:?}",
        start_of_messages
    );
}
