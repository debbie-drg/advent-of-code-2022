use std::cmp;
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

struct Reservoir<'a> {
    filled_positions: HashMap<Vec<i32>, &'a str>,
    sand_source: Vec<i32>,
    left: i32,
    right: i32,
    top: i32,
    bottom: i32,
}

impl Reservoir<'_> {
    fn populate(&mut self, rock_traces: Vec<Vec<Vec<i32>>>) {
        rock_traces.iter().for_each(|rock_trace| {
            for index in 0..rock_trace.len() {
                self.add_rock(rock_trace[index].clone(), false);
                if index > 0 {
                    self.add_line(&rock_trace[index - 1], &rock_trace[index]);
                }
            }
        });
        self.find_extremes();
    }

    fn find_extremes(&mut self) {
        let mut bottom = self.bottom.clone();
        let mut top = self.top.clone();
        let mut left = self.left.clone();
        let mut right = self.right.clone();
        self.filled_positions.keys().for_each(|position| {
            bottom = cmp::max(bottom, position[1]);
            top = cmp::min(top, position[1]);
            left = cmp::min(left, position[0]);
            right = cmp::max(right, position[0]);
        });
        self.bottom = bottom;
        self.top = top;
        self.left = left;
        self.right = right;
    }

    fn add_sand_grain(&mut self, line_added: bool) -> bool {
        let mut sand_position = self.sand_source.clone();
        loop {
            if (line_added == true) & (sand_position[1] == self.bottom - 1) {
                self.add_rock(vec![sand_position[0], self.bottom], true);
                self.add_rock(vec![sand_position[0] - 1, self.bottom], true);
                self.add_rock(vec![sand_position[0] + 1, self.bottom], true);
                self.add_sand(sand_position);
                return false;
            }
            if sand_position[1] == self.bottom {
                return true;
            }
            if !self
                .filled_positions
                .contains_key(&vec![sand_position[0], sand_position[1] + 1])
            {
                sand_position[1] += 1;
            } else if !self
                .filled_positions
                .contains_key(&vec![sand_position[0] - 1, sand_position[1] + 1])
            {
                sand_position[0] -= 1;
                sand_position[1] += 1;
            } else if !self
                .filled_positions
                .contains_key(&vec![sand_position[0] + 1, sand_position[1] + 1])
            {
                sand_position[0] += 1;
                sand_position[1] += 1;
            } else {
                let truth_value = sand_position == self.sand_source;
                self.add_sand(sand_position);
                return truth_value;
            }
        }
    }

    fn add_rock(&mut self, rock_pos: Vec<i32>, check: bool) {
        if check == true {
            if self.filled_positions.contains_key(&rock_pos) {
                return;
            }
            self.left = cmp::min(self.left, rock_pos[0]);
            self.right = cmp::max(self.right, rock_pos[0]);
        }
        self.filled_positions.insert(rock_pos, "rock");
    }

    fn add_sand(&mut self, sand_pos: Vec<i32>) {
        self.filled_positions.insert(sand_pos, "sand");
    }

    fn add_floor_line(&mut self) {
        for index in self.left..self.right + 1 {
            self.add_rock(vec![index, self.bottom + 2], false);
        }
        self.bottom = self.bottom + 2;
    }

    fn add_line(&mut self, rock_1: &Vec<i32>, rock_2: &Vec<i32>) {
        if (rock_1[0] == rock_2[0]) == (rock_1[1] == rock_2[1]) {
            return;
        }
        if rock_1[0] != rock_2[0] {
            let right = rock_1[1];
            let min_left = cmp::min(rock_1[0], rock_2[0]);
            let max_left = cmp::max(rock_1[0], rock_2[0]);
            for left in min_left + 1..max_left {
                self.add_rock(vec![left, right], false);
            }
        }
        if rock_1[1] != rock_2[1] {
            let left = rock_1[0];
            let min_right = cmp::min(rock_1[1], rock_2[1]);
            let max_right = cmp::max(rock_1[1], rock_2[1]);
            for right in min_right + 1..max_right {
                self.add_rock(vec![left, right], false);
            }
        }
    }

    fn fill_until_drop(&mut self) -> usize {
        let mut index = 0;
        loop {
            if self.add_sand_grain(false) == true {
                return index;
            }
            index += 1;
        }
    }

    fn fill_until_source_covered(&mut self, start_index: usize) -> usize {
        let mut index = start_index;
        self.add_floor_line();
        loop {
            index += 1;
            if self.add_sand_grain(true) == true {
                return index;
            }
        }
    }
}

fn preprocess_input(input_data: String) -> Vec<Vec<Vec<i32>>> {
    let mut rock_positions: Vec<Vec<Vec<i32>>> = vec![];
    let split_data: Vec<&str> = input_data.split("\n").collect();
    for data_line in split_data {
        let mut current_rock_positions: Vec<Vec<i32>> = vec![];
        data_line.replace("->", "").split("  ").for_each(|element| {
            current_rock_positions.push(
                element
                    .split(",")
                    .map(|number| number.parse::<i32>().unwrap())
                    .collect(),
            )
        });
        rock_positions.push(current_rock_positions);
    }
    rock_positions
}

fn main() {
    let data = get_data();
    let rock_positions = preprocess_input(data);
    let mut reservoir = Reservoir {
        filled_positions: HashMap::new(),
        sand_source: vec![500, 0],
        left: 0,
        right: 1000,
        top: 1000,
        bottom: 0,
    };
    reservoir.populate(rock_positions);
    let steps_until_drop = reservoir.fill_until_drop();
    println!(
        "Last sitting grain of sand after {} time units.",
        steps_until_drop
    );

    let steps_until_covered = reservoir.fill_until_source_covered(steps_until_drop);
    println!(
        "Sand blocks the source after {} time units.",
        steps_until_covered
    );
}
