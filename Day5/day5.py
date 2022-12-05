from copy import deepcopy


class Port:
    def __init__(self, cranes: str, mode_9001: bool = False):
        cranes = cranes.split("\n")
        stack_values = [element for element in cranes[-1] if element != " "]
        stacks = {key: [] for key in stack_values}
        positions = [cranes[-1].index(stack) for stack in stacks]

        for line in cranes[-2::-1]:
            for index, element in enumerate(stacks):
                contents = line[positions[index]]
                if contents != " ":
                    stacks[element].append(line[positions[index]])

        self.status = stacks
        self.mode_9001 = mode_9001

    def move(self, number: int, move_from: str, move_to: str):
        elements_to_move = self.status[move_from][-number:]
        del self.status[move_from][-number:]
        if not self.mode_9001:
            elements_to_move.reverse()
        self.status[move_to] += elements_to_move

    def print_top(self) -> str:
        top_elements = ""
        for key in self.status:
            top_elements += self.status[key][-1]
        return top_elements


def extract_moves(moves: str) -> list:
    moves = moves.split("\n")
    moves.remove("")
    moves = [line.split(" ") for line in moves]
    moves = [[int(line[1]), line[3], line[5]] for line in moves]
    return moves


if __name__ == "__main__":
    cranes, moves = open("input.txt").read().split(sep="\n\n")
    moves = extract_moves(moves)
    stacks_9000 = Port(cranes)
    stacks_9001 = deepcopy(stacks_9000)
    stacks_9001.mode_9001 = True
    for move in moves:
        stacks_9000.move(*move)
        stacks_9001.move(*move)

    print(
        f"The elements at the top after moving with CrateMover 9000 are {stacks_9000.print_top()}"
    )
    print(
        f"The elements at the top after moving with CrateMover 9001 are {stacks_9001.print_top()}"
    )
