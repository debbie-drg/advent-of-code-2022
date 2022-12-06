use std::collections::HashSet;
use std::fs::File;
use std::io::Read;

fn load_file(file_name: &str) -> String {
    let mut file = File::open(file_name).expect("File not found.");
    let mut data = String::new();
    file.read_to_string(&mut data).expect("File not found.");
    return data.trim_end().to_string();
}

fn detect_first_marker(datastream: &str, length_of_indicator: usize) -> usize {
    let loop_length = datastream.len() - length_of_indicator;
    for index in 0..loop_length {
        let slice = &datastream[index..index + length_of_indicator];
        let hashset = slice.chars().collect::<HashSet<_>>();
        if hashset.len() == length_of_indicator {
            return index + length_of_indicator;
        }
    }
    return 0;
}

fn main() {
    let data = load_file("input.txt");
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
