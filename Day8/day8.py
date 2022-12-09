import numpy as np
import sys


def read_array(text_input: str) -> np.ndarray:
    text_input_split = text_input.split("\n")
    text_input_split.remove("")
    return np.array([list(row) for row in text_input_split], dtype=int)


def view_distance_left(
    tree_heights: np.ndarray, row: int, column: int
) -> tuple[int, bool]:
    for index in range(column - 1, -1, -1):
        if tree_heights[row, column] <= tree_heights[row, index]:
            return column - index, False
    return column, tree_heights[row, column] > tree_heights[row, 0]


def view_distance_right(
    tree_heights: np.ndarray, row: int, column: int
) -> tuple[int, bool]:
    for index in range(column + 1, tree_heights.shape[1]):
        if tree_heights[row, column] <= tree_heights[row, index]:
            return (index - column, False)
    return (
        tree_heights.shape[1] - column - 1,
        tree_heights[row, column] > tree_heights[row, tree_heights.shape[1] - 1],
    )


def view_distance_up(
    tree_heights: np.ndarray, row: int, column: int
) -> tuple[int, bool]:
    for index in range(row - 1, -1, -1):
        if tree_heights[row, column] <= tree_heights[index, column]:
            return (row - index, False)
    return (row, tree_heights[row, column] > tree_heights[0, column])


def view_distance_down(
    tree_heights: np.ndarray, row: int, column: int
) -> tuple[int, bool]:
    for index in range(row + 1, tree_heights.shape[0]):
        if tree_heights[row, column] <= tree_heights[index, column]:
            return (index - row, False)
    return (
        tree_heights.shape[0] - row - 1,
        tree_heights[row, column] > tree_heights[tree_heights.shape[0] - 1, column],
    )


def view_distances_and_scenic_scores(
    trees: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    array_shape = trees.shape
    visible_filter = np.full(trees.shape, True)
    scores = np.empty((array_shape[0] - 2, array_shape[1] - 2), dtype=int)
    for row in range(1, array_shape[0] - 1):
        for column in range(1, array_shape[1] - 1):
            scenic_score = 1
            visible = False

            this_score, this_visible = view_distance_left(trees, row, column)
            scenic_score *= this_score
            visible = visible or this_visible

            this_score, this_visible = view_distance_right(trees, row, column)
            scenic_score *= this_score
            visible = visible or this_visible

            this_score, this_visible = view_distance_up(trees, row, column)
            scenic_score *= this_score
            visible = visible or this_visible

            this_score, this_visible = view_distance_down(trees, row, column)
            scenic_score *= this_score
            visible = visible or this_visible

            visible_filter[row, column] = visible
            scores[row - 1, column - 1] = scenic_score
    return visible_filter, scores


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    trees = read_array(open(file_name).read())
    visible_filter, scenic_scores = view_distances_and_scenic_scores(trees)

    number_visible = np.sum(visible_filter)

    print(f"The number of visible trees is {number_visible}.")

    max_score = np.max(scenic_scores)

    print(f"The possible maximum scenic score is {max_score}.")
