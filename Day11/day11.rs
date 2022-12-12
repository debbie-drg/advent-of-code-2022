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

struct Monkey {
    test_modulo: u64,
    pub holding_items: Vec<u64>,
    global_modulo: u64,
    divide_worry: bool,
    pub items_inspected: u64,
    worry_operation_marker: char,
    worry_operation_value: u64,
    monkey_if_true: usize,
    monkey_if_false: usize,
}

impl Monkey {
    fn update_worry_values(&mut self) {
        if self.worry_operation_value == 0 {
            self.holding_items = self
                .holding_items
                .iter()
                .map(|element| element * element)
                .collect();
        } else {
            match self.worry_operation_marker {
                '*' => {
                    self.holding_items = self
                        .holding_items
                        .iter()
                        .map(|element| {
                            element * self.worry_operation_value
                        })
                        .collect()
                }
                '+' => {
                    self.holding_items = self
                        .holding_items
                        .iter()
                        .map(|element| {
                            element + self.worry_operation_value
                        })
                        .collect()
                }
                _ => panic!("Wrong operation marker"),
            }
        }
        if self.divide_worry {
            self.holding_items = self
                .holding_items
                .iter()
                .map(|element| element / 3)
                .collect();
        } else {
            self.holding_items = self
                .holding_items
                .iter()
                .map(|element| element.rem_euclid(self.global_modulo))
                .collect();
        }
        self.items_inspected += self.holding_items.len() as u64;
    }

    fn monkey_to_pass(&self, element: &u64) -> usize {
        if element.rem_euclid(self.test_modulo) == 0 {
            return self.monkey_if_true;
        } else {
           return self.monkey_if_false;
        }
    }
}

struct KeepAway {
    monkeys: Vec<Monkey>,
}

impl KeepAway {
    fn add_monkey(&mut self, commands: &str, divide_worry: bool) {
        let worry_operation_value: u64;
        let parsed_commands = split_lines(commands);

        if parsed_commands[2].last().unwrap() == &"old" {
            worry_operation_value = 0
        } else {
            worry_operation_value = parsed_commands[2].last().unwrap().parse::<u64>().unwrap();
        }

        let mut holding_items = vec![];
        for index in 2..parsed_commands[1].len() - 1 {
            holding_items.push(
                parsed_commands[1][index]
                    .strip_suffix(",")
                    .unwrap()
                    .parse::<u64>()
                    .unwrap(),
            );
        }
        holding_items.push(parsed_commands[1].last().unwrap().parse::<u64>().unwrap());

        self.monkeys.push(Monkey {
            test_modulo: parsed_commands[3].last().unwrap().parse::<u64>().unwrap(),
            holding_items: holding_items,
            global_modulo: 0,
            divide_worry: divide_worry,
            items_inspected: 0,
            worry_operation_marker: parsed_commands[2][4].chars().next().unwrap(),
            worry_operation_value: worry_operation_value,
            monkey_if_true: parsed_commands[4].last().unwrap().parse::<usize>().unwrap(),
            monkey_if_false: parsed_commands[5].last().unwrap().parse::<usize>().unwrap(),
        })
    }

    fn add_all_monkeys(&mut self, commands: &Vec<&str>, divide_worry: bool) {
        for command in commands {
            self.add_monkey(command, divide_worry);
        }
        self.set_global_modulo();
    }

    fn set_global_modulo(&mut self) {
        let mut global_modulo: u64 = 1;
        for monkey in self.monkeys.iter() {
            global_modulo *= monkey.test_modulo;
        }
        for monkey in self.monkeys.iter_mut() {
            monkey.global_modulo = global_modulo;
        }
    }

    fn keep_away_round(&mut self) {
        for monkey_index in 0..self.monkeys.len() {
            self.monkeys[monkey_index].update_worry_values();
            for _ in 0..self.monkeys[monkey_index].holding_items.len() {
                let item = self.monkeys[monkey_index].holding_items.pop().unwrap();
                let recipient_monkey = self.monkeys[monkey_index].monkey_to_pass(&item);
                self.monkeys[recipient_monkey].holding_items.push(item);
            }
        }
    }

    fn play_multiple_rounds(&mut self, number_rounds: usize) {
        for _ in 0..number_rounds {
            self.keep_away_round();
        }
    }

    fn times_inspected_items(&self) -> Vec<u64> {
        let mut times_inspected = vec![];
        for monkey in &self.monkeys {
            times_inspected.push(monkey.items_inspected);
        }
        times_inspected
    }

    fn monkey_business(&self) -> u64 {
        let mut times_inspected = self.times_inspected_items();
        times_inspected.sort_unstable();
        times_inspected.reverse();
        times_inspected[0] * times_inspected[1]
    }
}

fn split_lines<'a>(lines: &'a str) -> Vec<Vec<&'a str>> {
    let mut split_lines_vec: Vec<Vec<&str>> = vec![];
    let split_lines: Vec<&str> = lines.split("\n").collect();
    for line in split_lines {
        let trimmed_line: &str = line.trim();
        split_lines_vec.push(trimmed_line.split(" ").collect());
    }
    split_lines_vec
}

fn main() {
    let data = get_data();
    let split_data: Vec<&str> = data.split("\n\n").collect();
    let mut keep_away = KeepAway { monkeys: vec![] };
    keep_away.add_all_monkeys(&split_data, true);
    keep_away.play_multiple_rounds(20);

    println!(
        "The monkey business after 20 rounds is {}.",
        keep_away.monkey_business()
    );

    let mut keep_away = KeepAway { monkeys: vec![] };
    keep_away.add_all_monkeys(&split_data, false);
    keep_away.play_multiple_rounds(10000);

    println!(
        "The monkey business after 10000 rounds with no division is {}.",
        keep_away.monkey_business()
    )
}
