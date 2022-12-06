from copy import deepcopy
import sys

class Port:
    def __init__(self, cranes: str, mode_9001: bool = False):
        split_cranes = cranes.split("\n")
        stack_values = [element for element in split_cranes[-1] if element != " "]
        stacks = [[] for _ in stack_values]
        self.positions = [split_cranes[-1].index(value) for value in stack_values]

        for line in split_cranes[-2::-1]:
            for index in range(len(stacks)):
                contents = line[self.positions[index]]
                if contents != " ":
                    stacks[index].append(line[self.positions[index]])

        self.status = stacks
        self.mode_9001 = mode_9001

    def move(self, number: int, move_from: int, move_to: int):
        elements_to_move = self.status[move_from][-number:]
        del self.status[move_from][-number:]
        if not self.mode_9001:
            elements_to_move.reverse()
        self.status[move_to] += elements_to_move

    def print_top(self) -> str:
        top_elements = ""
        for stack in self.status:
            top_elements += stack[-1]
        return top_elements

    def represent_stack(self) -> str:
        stack_representation = ""
        for index in range(len(self.status)):
            stack_representation += f" {index + 1}  "
        finished = [False] * len(self.status)
        height = 0
        while not all(finished):
            current_line = ""
            for index in range(len(finished)):
                if len(self.status[index]) > height:
                    current_line += f"[{self.status[index][height]}] "
                else:
                    current_line += "    "
                    finished[index] = True
            stack_representation = current_line + "\n" + stack_representation
            height += 1
        return stack_representation


def extract_moves(moves: str) -> list[list[int]]:
    split_moves = moves.split("\n")
    split_moves.remove("")
    split_moves = [line.split(" ") for line in split_moves]
    split_moves = [
        [int(line[1]), int(line[3]) - 1, int(line[5]) - 1] for line in split_moves
    ]
    return split_moves


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    cranes, moves = open(file_name).read().split(sep="\n\n")
    moves = extract_moves(moves)
    stacks_9000 = Port(cranes)
    stacks_9001 = deepcopy(stacks_9000)
    stacks_9001.mode_9001 = True
    for move in moves:
        stacks_9000.move(*move)
        stacks_9001.move(*move)

    print(
        f"The elements at the top after moving with CrateMover 9000 are {stacks_9000.print_top()}."
    )
    print(
        f"The elements at the top after moving with CrateMover 9001 are {stacks_9001.print_top()}."
    )

    #print("\nThis is how things are once CrateMover 9000 is done.")
    #print(stacks_9000.represent_stack())

    #print("\nThis is how things are once CrateMover 9001 is done.")
    #print(stacks_9001.represent_stack())