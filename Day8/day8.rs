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

fn view_distance_left(tree_heights: &Vec<Vec<u8>>, row: usize, column: usize) -> (u32, bool) {
    for index in (0..column).rev() {
        if tree_heights[row][column] <= tree_heights[row][index] {
            return ((column - index) as u32, false);
        }
    }
    return (column as u32, tree_heights[row][column] > tree_heights[row][0])
}

fn view_distance_right(tree_heights: &Vec<Vec<u8>>, row: usize, column: usize) -> (u32, bool) {
    for index in column + 1..tree_heights[0].len() {
        if tree_heights[row][column] <= tree_heights[row][index] {
            return ((index - column) as u32, false);
        }
    }
    return ((tree_heights[0].len() - column - 1) as u32, tree_heights[row][column] > tree_heights[row][tree_heights[0].len() - 1])
}

fn view_distance_up(tree_heights: &Vec<Vec<u8>>, row: usize, column: usize) -> (u32, bool) {
    for index in (0..row).rev() {
        if tree_heights[row][column] <= tree_heights[index][column] {
            return ((row - index) as u32, false);
        }
    }
    return (row as u32, tree_heights[row][column] > tree_heights[0][column])
}

fn view_distance_down(tree_heights: &Vec<Vec<u8>>, row: usize, column: usize) -> (u32, bool) {
    for index in row + 1..tree_heights.len() {
        if tree_heights[row][column] <= tree_heights[index][column] {
            return ((index - row) as u32, false);
        }
    }
    return ((tree_heights.len() - row - 1) as u32, tree_heights[row][column] > tree_heights[tree_heights.len() - 1][column])
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
            let mut scenic_score: u32 = 1;
            let mut _scenic_score: u32;
            let mut visible: bool = false;
            let mut _visible: bool;

            (_scenic_score, _visible) = view_distance_left(&tree_heights, row, column);
            scenic_score *= _scenic_score;
            visible = visible | _visible;

            (_scenic_score, _visible) = view_distance_right(&tree_heights, row, column);
            scenic_score *= _scenic_score;
            visible = visible | _visible;

            (_scenic_score, _visible) = view_distance_up(&tree_heights, row, column);
            scenic_score *= _scenic_score;
            visible = visible | _visible;

            (_scenic_score, _visible) = view_distance_down(&tree_heights, row, column);
            scenic_score *= _scenic_score;
            visible = visible | _visible;

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
    println!("The possible maximum scenic score is {}.", highest_scenic_score)
}