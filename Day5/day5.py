from copy import deepcopy


def extract_stacks(cranes: str) -> dict():
    cranes = cranes.split("\n")
    stack_values = [element for element in cranes[-1] if element != " "]
    stacks = {key: [] for key in stack_values}
    positions = [cranes[-1].index(stack) for stack in stacks]

    for line in cranes[-2::-1]:
        for index, element in enumerate(stacks):
            contents = line[positions[index]]
            if contents != " ":
                stacks[element].append(line[positions[index]])

    return stacks


def extract_moves(moves: str) -> list:
    moves = moves.split("\n")
    moves.remove("")
    moves = [line.split(" ") for line in moves]
    moves = [[int(line[1]), line[3], line[5]] for line in moves]
    return moves


def move(moves: list, stacks: dict, reverse: bool = True):
    for move in moves:
        elements_to_move = stacks[move[1]][-move[0]:]
        del stacks[move[1]][-move[0]:]
        if reverse:
            elements_to_move.reverse()
        stacks[move[2]] += elements_to_move


def print_top(stacks: dict) -> str:
    top_elements = ""
    for key in stacks:
        top_elements += stacks[key][-1]
    return top_elements


if __name__ == "__main__":
    cranes, moves = open("input.txt").read().split(sep="\n\n")
    moves = extract_moves(moves)
    stacks_9000 = extract_stacks(cranes)
    stacks_9001 = deepcopy(stacks_9000)
    move(moves, stacks_9000)
    move(moves, stacks_9001, reverse=False)

    print(
        f"The elements at the top after moving with CrateMover 9000 are {print_top(stacks_9000)}"
    )
    print(
        f"The elements at the top after moving with CrateMover 9001 are {print_top(stacks_9001)}"
    )