import sys
import numpy as np

MOVE_CORRESPONDENCE = {
    "R": np.array([1, 0], dtype=int),
    "L": np.array([-1, 0], dtype=int),
    "U": np.array([0, 1], dtype=int),
    "D": np.array([0, -1], dtype=int),
}


def grid_distance(head, tail):
    return np.max(np.abs(head - tail))


def move(rope, command, positions_visited):
    global MOVE_CORRESPONDENCE
    head_move = MOVE_CORRESPONDENCE[command[0]]
    for _ in range(command[1]):
        rope[0] += head_move
        for index in range(1, rope.shape[0]):
            if grid_distance(rope[index - 1], rope[index]) <= 1:
                break
            rope[index] += np.sign(rope[index - 1] - rope[index])
            positions_visited.add(tuple(rope[-1]))
    return rope, positions_visited


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"

    rope_1 = np.zeros((2, 2), dtype=int)
    positions_visited_1 = {(0, 0)}

    rope_2 = np.zeros((10, 2), dtype=int)
    positions_visited_2 = {(0, 0)}

    with open(file_name) as commands:
        for command in commands:
            command = command.split(" ")
            command[1] = int(command[1])

            rope_1, positions_visited_1 = move(rope_1, command, positions_visited_1)

            rope_2, positions_visited_2 = move(rope_2, command, positions_visited_2)

    print(f"The tail visited {len(positions_visited_1)} positions in part one.")
    print(f"The tail visited {len(positions_visited_2)} positions in part two.")
