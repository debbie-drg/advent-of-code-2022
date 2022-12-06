const VALUE_A: u8 = b'a';

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

fn _detect_first_marker_old(datastream: &str, length_of_indicator: usize) -> usize {
    return datastream
        .as_bytes()
        .windows(length_of_indicator)
        .position(|window| {
            window
                .iter()
                .enumerate()
                .all(|(idx, c)| !window[..idx].contains(c))
        })
        .unwrap()
        + length_of_indicator;
}

fn detect_first_marker(datastream: &str, length_of_indicator: usize) -> usize {
    // We use a sliding window
    let mut counts = [0u32; 26];
    let mut unique = 0;

    let bytesstream = datastream.as_bytes();

    // We populate with the first letters, up to the length of the indicator
    for index in 0..length_of_indicator {
        let character = (bytesstream[index] - VALUE_A) as usize;

        counts[character] += 1;
        if counts[character] == 1 {
            unique += 1;
        }
    }

    if unique == length_of_indicator {
        return length_of_indicator;
    }

    // Now we update the amount of unique elements and counts by a sliding window.

    let iterator_limit = bytesstream.len() - length_of_indicator - 1;

    for index in 0..iterator_limit {
        let leaving_character = (&bytesstream[index] - VALUE_A) as usize;
        counts[leaving_character] -= 1;
        if counts[leaving_character] == 0 {
            unique -= 1;
        }
        let entering_character = (&bytesstream[index + length_of_indicator] - VALUE_A) as usize;
        counts[entering_character] += 1;
        if counts[entering_character] == 1 {
            unique += 1;
        }
        if unique == length_of_indicator {
            return index + length_of_indicator + 1;
        }
    }
    
    panic!("The start message does not exist.")

    /* This is a more elegant approach to express this that I saw around.
        bytesstream
        .windows(length_of_indicator + 1) // We add one to remove the leaving letter
        .enumerate()
        .find(|&(_index, window)| {
            let character = (&window[0] - VALUE_A) as usize;
            counts[character] -= 1;
            if counts[character] == 0 {
                unique -= 1;
            }
            let character = (&window[length_of_indicator] - VALUE_A) as usize;
            counts[character] += 1;
            if counts[character] == 1 {
                unique += 1;
            }

            unique == length_of_indicator
        })
        .map(|(index, _window)| index + length_of_indicator + 1)
        .unwrap() */
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
