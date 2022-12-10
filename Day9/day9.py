import sys

MOVE_CORRESPONDENCE = {
    "R": [1, 0],
    "L": [-1, 0],
    "U": [0, 1],
    "D": [0, -1],
}


def preprocess_commands(commands):
    commands = commands.split("\n")
    commands.remove("")
    commands = [command.split(" ") for command in commands]
    commands = [[command[0], int(command[1])] for command in commands]
    return commands


def grid_distance(head, tail):
    return max([abs(head[0] - tail[0]), abs(head[1] - tail[1])])


def add_vectors(vector_1: list, vector_2: list) -> list:
    return [vector_1[index] + vector_2[index] for index in range(len(vector_1))]


def substract_vectors(vector_1: list, vector_2: list) -> list:
    return [vector_1[index] - vector_2[index] for index in range(len(vector_1))]


def make_ones(vector: list) -> list:
    ones_vector = [0] * len(vector)
    for index in range(len(vector)):
        try:
            ones_vector[index] = vector[index]/abs(vector[index])
        except ZeroDivisionError:
            ones_vector[index] = 0
    return ones_vector


def move_step(rope, command, positions_visited):
    global MOVE_CORRESPONDENCE
    for _ in range(command[1]):
        rope[0] = add_vectors(rope[0], MOVE_CORRESPONDENCE[command[0]])
        for index in range(1, len(rope)):
            if grid_distance(rope[index - 1], rope[index]) <= 1:
                break
            rope[index] = add_vectors(rope[index], make_ones(substract_vectors(rope[index-1], rope[index])))
            positions_visited.add(tuple(rope[-1]))
    return rope, positions_visited


def move_all(commands, rope_length):
    rope = [[0,0] for _ in range(rope_length)]
    positions_visited = {(0, 0)}
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
