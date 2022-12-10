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

fn check_sprite(cycle_count: &i32, registry: &i32) -> bool {
    let position = cycle_count.rem_euclid(40);
    if (position == registry - 1) | (position == *registry) | (position == registry + 1) {
        return true
    }
    return false
}

fn pixel(is_on: bool) -> char {
    if is_on {
        return '#';
    } else {
        return  '.';
    }
}

fn check_new_line(cycle_count: &i32) -> bool {
    return cycle_count.rem_euclid(40) == 0
}

fn render_display(instructions: &Vec<&str>) -> (i32, String) {
    let mut display = String::new();
    let mut registry_x: i32 = 1;
    let mut strength_sum: i32 = 0;
    let mut cycle_count: i32 = 0;

    for instruction in instructions {
        let split_instruction: Vec<&str> = instruction.split(" ").collect();
        if check_new_line(&cycle_count) == true {
            display.push('\n');
        }
        display.push(pixel(check_sprite(&cycle_count, &registry_x)));
        cycle_count += 1;
        if cycle_count.rem_euclid(40) == 20 {
            strength_sum += cycle_count * registry_x
        }
        if split_instruction.len() == 2 {
            if check_new_line(&cycle_count) == true {
                display.push('\n');
            }
            display.push(pixel(check_sprite(&cycle_count, &registry_x)));
            cycle_count += 1;
            if cycle_count.rem_euclid(40) == 20 {
                strength_sum += cycle_count * registry_x
            }
            registry_x += split_instruction[1].parse::<i32>().unwrap();
        }
    }
    return (strength_sum, display)
}


fn main() {
    let data = get_data();
    let split_data: Vec<&str> = data.split("\n").collect();

    let (strength_sum, display) = render_display(&split_data);
    println!("The signal strength is {}", strength_sum);
    println!("\nThis is what the display looks like!");
    println!("{}", display)
}