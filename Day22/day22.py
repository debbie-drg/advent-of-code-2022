import sys

DIRECTION_VALUES = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_instructions(instructions: str) -> list:
    parsed_instructions = []
    number_buffer = ""
    for character in instructions:
        if character in ["R", "L"]:
            parsed_instructions.append(int(number_buffer))
            parsed_instructions.append(character)
            number_buffer = ""
        else:
            number_buffer += character
    return parsed_instructions


class Jungle:
    def __init__(self, terrain: list[str]):
        self.terrain = set()
        self.wall = set()
        for vertical_index, line in enumerate(terrain):
            for horizontal_index in range(len(line)):
                if line[horizontal_index] == " ":
                    continue
                self.terrain.add((horizontal_index, vertical_index))
                if line[horizontal_index] == "#":
                    self.wall.add((horizontal_index, vertical_index))
        self.position = self.start_position()
        self.cube_size = int((len(self.terrain)//6) ** (1/2))

    def start_position(self):
        vertical_index = 0
        horizontal_index = min(
            [position[0] for position in list(self.terrain) if position[1] == 0]
        )
        return horizontal_index, vertical_index

    @staticmethod
    def next_position(position: tuple[int, int], direction: tuple[int, int]):
        return (position[0] + direction[0], position[1] + direction[1])

    def move(self, direction: tuple[int, int], number_moves: int):
        for _ in range(number_moves):
            next_position = self.next_position(self.position, direction)
            if self.next_position(self.position, direction) in self.terrain:
                if next_position in self.wall:
                    return None
                self.position = next_position
            else:
                next_position, wrap = self.wrap_around(direction)
                if not wrap:
                    return None
                self.position = next_position

    def wrap_around(self, direction: tuple[int, int]) -> tuple[tuple[int, int], bool]:
        current_position = self.position
        opposite_direction = (-1 * direction[0], -1 * direction[1])
        next_position = self.next_position(current_position, opposite_direction)
        while next_position in self.terrain:
            current_position = next_position
            next_position = self.next_position(current_position, opposite_direction)
        if current_position in self.wall:
            return current_position, False
        return current_position, True
    
    def password(self) -> int:
        return 1000 * (self.position[1] + 1) + 4 * (self.position[0] + 1) + self.direction_index

    def path_move(self, instructions):
        self.direction_index = 0
        for instruction in instructions:
            if isinstance(instruction, int):
                self.move(DIRECTION_VALUES[self.direction_index], instruction)
            else:
                match instruction:
                    case "R":
                        self.direction_index += 1
                    case "L":
                        self.direction_index -= 1
                self.direction_index %= len(DIRECTION_VALUES)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().splitlines()
    terrain, moves = input_data[:-2], input_data[-1]

    jungle = Jungle(terrain)
    instructions = parse_instructions(moves)
    jungle.path_move(instructions)
    print(f"The password is {jungle.password()}.")

