const VALUE_A: u32 = b'a' as u32;

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

fn row_col_to_pos(row: &usize, col: &usize, number_cols: &usize) -> usize {
    row * number_cols + col
}

fn pos_to_row_col(pos: &usize, number_cols: &usize) -> (usize, usize) {
    (pos / number_cols, pos.rem_euclid(*number_cols))
}

fn check_neiboughrs(
    elevation_map: &[u8],
    position: &usize,
    number_rows: &usize,
    number_cols: &usize,
) -> Vec<usize> {
    let mut neighbours = vec![];
    let current_altitude = elevation_map[*position] as u32 - VALUE_A;
    let number_elements = number_rows * number_cols;
    let (row, column) = pos_to_row_col(&position, &number_cols);

    if row > 0 {
        let top = row_col_to_pos(&(row - 1), &column, &number_cols);
        if (elevation_map[top] as u32) >= current_altitude + VALUE_A - 1 {
            neighbours.push(top);
        }
    }

    if position > &0 {
        let left = position - 1;
        if (elevation_map[left] as u32) >= current_altitude + VALUE_A - 1 {
            neighbours.push(left);
        }
    }

    let bottom = row_col_to_pos(&(row + 1), &column, &number_cols);
    if bottom < number_elements {
        if (elevation_map[bottom] as u32) >= current_altitude + VALUE_A - 1 {
        neighbours.push(bottom);
        }
    }

    let right = position + 1;
    if right < number_elements {
        if (elevation_map[right] as u32) >= current_altitude + VALUE_A - 1 {
            neighbours.push(right);
        }
    }

    neighbours
}

struct Position {
    altitude: u32,
    neighbours: Vec<usize>,
    _position: usize,
    distance_to_end: u32,
}

struct Terrain {
    number_rows: usize,
    number_cols: usize,
    positions: Vec<Position>,
    start: usize,
    end: usize,
    distances_computed: bool,
}

impl Terrain {
    fn build_terrain(&mut self, elevation_map: String) {
        let split_map: Vec<&str> = elevation_map.split("\n").collect();
        self.number_rows = split_map.len();
        self.number_cols = split_map[0].len();
        let elevation_map_stripped = str::replace(&elevation_map, "\n", "");
        let elevation_only_map = elevation_map_stripped.replace("S", "a").replace("E", "z");
        let elevation_map_as_bytes = elevation_only_map.as_bytes();
        let number_elements = (self.number_cols * self.number_rows) as u32;
        let mut distance_to_end = 0;
        let mut altitude;

        for (index, element) in elevation_map_stripped.as_bytes().iter().enumerate() {
            if element == &b'S' {
                self.start = index;
                altitude = b'a' as u32 - VALUE_A;
            } else if element == &b'E' {
                self.end = index;
                distance_to_end = 0;
                altitude = b'z' as u32 - VALUE_A;
            } else {
                distance_to_end = number_elements;
                altitude = *element as u32 - VALUE_A;
            }

            let neighbours = check_neiboughrs(
                &elevation_map_as_bytes,
                &index,
                &self.number_rows,
                &self.number_cols,
            );

            self.positions.push(Position {
                altitude: altitude,
                neighbours: neighbours,
                _position: index,
                distance_to_end: distance_to_end,
            });
        }
    }

    fn distance_start_to_end(&mut self) -> u32 {
        if self.distances_computed == false {
            self.compute_distances();
        }
        self.positions[self.start].distance_to_end
    }

    fn min_distance_from_bottom(&mut self) -> u32 {
        if self.distances_computed == false {
            self.compute_distances()
        }
        let mut distance = (self.number_rows * self.number_cols) as u32;
        for position in &self.positions {
            if position.altitude == 0 {
                distance = std::cmp::min(distance, position.distance_to_end)
            }
        }
        distance
    }

    fn compute_distances(&mut self) {
        self.distances_computed = true;
        let mut unvisited: Vec<usize> = (0..self.positions.len()).collect();
        let mut current_position = self.end;
        let mut tentative_distance;
        let max_distance = self.positions[self.start].distance_to_end;
        let mut min_unvisited_distance;
        while unvisited.len() > 0 {
            if current_position == self.start {
                break;
            }
            tentative_distance = self.positions[current_position].distance_to_end + 1;
            let current_neighbours = self.positions[current_position].neighbours.clone();
            for neighbour in current_neighbours {
                if unvisited.contains(&neighbour)
                    & (tentative_distance < self.positions[neighbour].distance_to_end)
                {
                    self.positions[neighbour].distance_to_end = tentative_distance;
                }
            }
            unvisited.remove(unvisited.iter().position(|x| *x == current_position).expect("Element not found"));
            min_unvisited_distance = max_distance;
            for position in &unvisited {
                if self.positions[*position].distance_to_end <= min_unvisited_distance {
                    current_position = *position;
                    min_unvisited_distance = self.positions[*position].distance_to_end;
                }
            }
        }
    }
}

fn main() {
    let data = get_data();
    let mut terrain_map = Terrain{
        number_rows: 0,
        number_cols: 0,
        positions: vec![],
        start: 0,
        end: 0,
        distances_computed: false,        
    };
    terrain_map.build_terrain(data);

    println!("The shortest path has length {}.", terrain_map.distance_start_to_end());
    println!("The closest point from the bottom is {} steps from the end.", terrain_map.min_distance_from_bottom());
}
