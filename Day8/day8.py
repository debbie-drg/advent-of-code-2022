import numpy as np
import sys


def read_array(text_input: str) -> np.ndarray:
    text_input_split = text_input.split("\n")
    text_input_split.remove("")
    return np.array([list(row) for row in text_input_split], dtype=int)


def four_directions(trees: np.ndarray, row: int, column: int) -> list[np.ndarray]:
    left = np.flip(trees[row, :column])
    right = trees[row, column + 1 :]
    up = np.flip(trees[:row, column])
    down = trees[row + 1 :, column]
    return [left, right, up, down]


def get_visible(trees: np.ndarray) -> np.ndarray:
    visible_filter = np.full(trees.shape, True)
    array_shape = trees.shape
    for row in range(1, array_shape[0] - 1):
        for column in range(1, array_shape[1] - 1):
            min_around = min(map(np.max, four_directions(trees, row, column)))
            visible_filter[row, column] = trees[row, column] > min_around
    return visible_filter


def view_distance(tree_height: int, direction: np.ndarray) -> int:
    try:
        return np.where(tree_height <= direction)[0][0] + 1
    except IndexError:  # Will happen if no tree blocks the view
        return direction.shape[0]


def scenic_score(height: int, directions: list[np.ndarray]) -> int:
    score = 1
    score *= view_distance(height, directions[0])
    score *= view_distance(height, directions[1])
    score *= view_distance(height, directions[2])
    score *= view_distance(height, directions[3])
    return score


def view_distances_and_scenic_scores(trees: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    array_shape = trees.shape
    visible_filter = np.full(trees.shape, True)
    scores = np.empty((array_shape[0] - 2, array_shape[1] - 2), dtype=int)
    for row in range(1, array_shape[0] - 1):
        for column in range(1, array_shape[1] - 1):
            directions = four_directions(trees, row, column)
            min_around = min(map(np.max, directions))
            visible_filter[row, column] = trees[row, column] > min_around            
            scores[row - 1, column - 1] = scenic_score(trees[row, column], directions)
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