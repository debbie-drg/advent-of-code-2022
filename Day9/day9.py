import sys
import numpy as np

MOVE_CORRESPONDENCE = {
    "R": np.array([1, 0], dtype=int),
    "L": np.array([-1, 0], dtype=int),
    "U": np.array([0, 1], dtype=int),
    "D": np.array([0, -1], dtype=int),
}


def preprocess_commands(commands):
    commands = commands.split("\n")
    commands.remove("")
    commands = [command.split(" ") for command in commands]
    commands = [[command[0], int(command[1])] for command in commands]
    return commands

def grid_distance(head, tail):
    return np.max(np.abs(head - tail))


def move_step(rope, command, positions_visited):
    global MOVE_CORRESPONDENCE
    for _ in range(command[1]):
        rope[0] += MOVE_CORRESPONDENCE[command[0]]
        for index in range(1, rope.shape[0]):
            if grid_distance(rope[index - 1], rope[index]) <= 1:
                break
            rope[index] += np.sign(rope[index - 1] - rope[index])
            positions_visited.add(tuple(rope[-1]))
    return rope, positions_visited


def move_all(commands, rope_length):
    rope = np.zeros((rope_length,2), dtype=int)
    positions_visited = {(0,0)}
    for command in commands:
        rope, positions_visited = move_step(rope, command, positions_visited)
    return positions_visited

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"

    commands = open(file_name).read()
    commands = preprocess_commands(commands)

    positions_visited_1 = move_all(commands, 2)
    positions_visited_2 = move_all(commands, 10)

    print(f"The tail visited {len(positions_visited_1)} positions in part one.")
    print(f"The tail visited {len(positions_visited_2)} positions in part two.")
