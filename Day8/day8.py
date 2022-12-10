import sys


def read_array(text_input: str) -> list:
    text_input_split = text_input.split("\n")
    text_input_split.remove("")
    return [list(row) for row in text_input_split]


def view_distance_left(
    tree_heights: list[list[int]], row: int, column: int
) -> tuple[int, bool]:
    for index in range(column - 1, -1, -1):
        if tree_heights[row][column] <= tree_heights[row][index]:
            return column - index, False
    return column, tree_heights[row][column] > tree_heights[row][0]


def view_distance_right(
    tree_heights: list[list[int]], row: int, column: int
) -> tuple[int, bool]:
    for index in range(column + 1, len(tree_heights[0])):
        if tree_heights[row][column] <= tree_heights[row][index]:
            return (index - column, False)
    return (
        len(tree_heights[0]) - column - 1,
        tree_heights[row][column] > tree_heights[row][len(tree_heights[0]) - 1],
    )


def view_distance_up(
    tree_heights: list[list[int]], row: int, column: int
) -> tuple[int, bool]:
    for index in range(row - 1, -1, -1):
        if tree_heights[row][column] <= tree_heights[index][column]:
            return (row - index, False)
    return (row, tree_heights[row][column] > tree_heights[0][column])


def view_distance_down(
    tree_heights: list[list[int]], row: int, column: int
) -> tuple[int, bool]:
    for index in range(row + 1, len(tree_heights)):
        if tree_heights[row][column] <= tree_heights[index][column]:
            return (index - row, False)
    return (
        len(tree_heights) - row - 1,
        tree_heights[row][column] > tree_heights[len(tree_heights) - 1][column],
    )


def view_distances_and_scenic_scores(
    trees: list[list[int]],
) -> tuple[list[list[int]], list[list[int]]]:
    number_rows, number_cols = len(trees), len(trees[0])
    visible_filter = [number_cols * [True]]
    scores = []
    for row in range(1, number_rows - 1):
        scores.append([])
        visible_filter.append([True])
        for column in range(1, number_cols):
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

            visible_filter[row].append(visible)
            scores[row - 1].append(scenic_score)
        visible_filter[row].append(True)
    visible_filter.append([True] * number_cols)
    return visible_filter, scores


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    trees = read_array(open(file_name).read())
    visible_filter, scenic_scores = view_distances_and_scenic_scores(trees)

    number_visible = sum([sum(row) for row in visible_filter])

    print(f"The number of visible trees is {number_visible}.")

    max_score = max([max(score) for score in scenic_scores])

    print(f"The possible maximum scenic score is {max_score}.")
