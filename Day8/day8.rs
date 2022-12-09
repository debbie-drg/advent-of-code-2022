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

fn get_left(tree_heights: &Vec<Vec<u8>>, row: usize, column: usize) -> Vec<u8> {
    let mut left = vec![];
    for index in 0..column {
        left.insert(0, tree_heights[row][index].clone());
    }
    left
}

fn get_right(tree_heights: &Vec<Vec<u8>>, row: usize, column: usize) -> Vec<u8> {
    let number_cols = tree_heights[0].len();
    let mut right = vec![];
    for index in column + 1..number_cols {
        right.push(tree_heights[row][index].clone());
    }
    right
}

fn get_up(tree_heights: &Vec<Vec<u8>>, row: usize, column: usize) -> Vec<u8> {
    let mut up = vec![];
    for index in 0..row {
        up.insert(0, tree_heights[index][column].clone());
    }
    up
}

fn get_down(tree_heights: &Vec<Vec<u8>>, row: usize, column: usize) -> Vec<u8> {
    let number_rows = tree_heights.len();
    let mut down = vec![];
    for index in row + 1..number_rows {
        down.push(tree_heights[index][column].clone());
    }
    down
}

fn all_directions(tree_heights: &Vec<Vec<u8>>, row: usize, column: usize) -> Vec<Vec<u8>> {
    let mut all_dirs = vec![];
    all_dirs.push(get_right(&tree_heights, row, column));
    all_dirs.push(get_left(&tree_heights, row, column));
    all_dirs.push(get_up(&tree_heights, row, column));
    all_dirs.push(get_down(&tree_heights, row, column));
    all_dirs
}

fn view_distance(tree_height: &u8, direction: &Vec<u8>) -> (u32, bool) {
    for index in 0..direction.len() {
        if tree_height <= &direction[index] {
            return ((index + 1) as u32, false);
        }
    }
    return (direction.len() as u32, tree_height > &direction[&direction.len() - 1]);
}

fn view_distances_and_scenic_scores(tree_heights: &Vec<Vec<u8>>) -> (Vec<Vec<bool>>, Vec<Vec<u32>>) {
    let mut visible_filter: Vec<Vec<bool>> = vec![];
    let mut scenic_scores: Vec<Vec<u32>> = vec![];
    let number_rows = tree_heights.len();
    let number_cols = tree_heights[0].len();
    visible_filter.push(vec![true; number_cols]);
    for row in 1..number_rows - 1 {
        visible_filter.push(vec![true]);
        scenic_scores.push(vec![]);
        for column in 1..number_cols - 1 {
            let four_directions = all_directions(&tree_heights, row, column);
            let mut scenic_score: u32 = 1;
            let mut _scenic_score: u32;
            let mut visible: bool = false;
            let mut _visible: bool;
            for direction in four_directions.iter() {
                (_scenic_score, _visible) = view_distance(&tree_heights[row][column], direction);
                scenic_score *= _scenic_score;
                if _visible == true {
                    visible = true;
                }
            }
            scenic_scores[row - 1].push(scenic_score);
            visible_filter[row].push(visible);
        }
        visible_filter.push(vec![true]);
    }
    visible_filter.push(vec![true; number_cols]);
    (visible_filter, scenic_scores)
}

fn main() {
    let data = get_data();
    let split_data = data.split("\n");
    let mut tree_heights: Vec<Vec<u8>> = vec![];
    for line in split_data {
        tree_heights.push(
            line.chars()
            .filter(|c| !c.is_whitespace())
            .map(|c| c.to_digit(10).unwrap() as u8)
            .collect::<Vec<_>>());
    }
    let (visible_filter, scenic_scores) = view_distances_and_scenic_scores(&tree_heights);
    let visible_trees: u32 = visible_filter
        .into_iter()
        .map(|row| row.into_iter().filter(|entry| *entry).count() as u32)
        .sum();
    
    let highest_scenic_score = scenic_scores
        .into_iter()
        .map(|row| row.into_iter().max().unwrap())
        .max()
        .unwrap();

    println!("The number of visible trees is {}.", visible_trees);
    println!("The maximum scenic score is {}.", highest_scenic_score)
}