use std::cmp::{Ord, Ordering, PartialEq, PartialOrd};
use std::str::from_utf8;

use Packet::*;

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


fn pairs_in_order(packets: &Vec<Packet>) -> usize {
    let mut answer = 0;

    packets.chunks(2).enumerate().for_each(|(index, pair)| {
        let first = &pair[0];
        let second = &pair[1];
        if first <= second {
            answer += index + 1;
        }
    });
    answer
}

fn decoder_key(packets: &Vec<Packet>) -> usize {

    let start_packet = parse_packet("[[2]]".as_bytes(), &mut 0);
    let end_packet = parse_packet("[[6]]".as_bytes(), &mut 0);

    let mut index_start = 1;
    let mut index_end = 2;

    packets.into_iter().for_each(|packet| {
        if packet <= &start_packet {
            index_start += 1;
            index_end += 1;
        } else if packet <= &end_packet {
            index_end += 1;
        }
    });
    index_start * index_end
}


#[derive(Clone, PartialEq, Eq)]
enum Packet {
    Int(usize),
    List(Vec<Self>),
}

fn parse_packet(string_line: &[u8], index: &mut usize) -> Packet {
    let mut packets = Vec::new();

    *index += 1;
    while string_line[*index] != b']' {
        if string_line[*index].is_ascii_digit() {
            let start = *index;
            while string_line[*index].is_ascii_digit() {
                *index += 1;
            }

            let val: usize = from_utf8(&string_line[start..*index]).unwrap().parse().unwrap();
            packets.push(Int(val))
        } else if string_line[*index] == b',' {
            *index += 1;
        } else if string_line[*index] == b'[' {
            packets.push(parse_packet(string_line, index));
        }
    }
    *index += 1;

    List(packets)
}

fn preprocess_input(input: String) -> Vec<Packet> {
    let mut packets: Vec<Packet> = vec![];
    input.replace("\n\n", "\n").split("\n").for_each(|line| {
        packets.push(parse_packet(&line.as_bytes(), &mut 0))
    });
    packets
}

impl Ord for Packet {
    fn cmp(&self, other: &Self) -> Ordering {
        match (self, other) {
            (Int(v1), Int(v2)) => v1.cmp(v2),
            (Int(v), List(_)) => List(vec![Int(*v)]).cmp(other),
            (List(_), Int(v)) => self.cmp(&List(vec![Int(*v)])),
            (List(packets1), List(packets2)) => packets1.cmp(packets2),
        }
    }
}

impl PartialOrd for Packet {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn main() {
    let input = get_data();
    let packets = preprocess_input(input);
    let in_order = pairs_in_order(&packets);
    let key = decoder_key(&packets);
    println!("The sum of indices of lists in order is {}", in_order);
    println!("The decoder key is {}.", key)
}
