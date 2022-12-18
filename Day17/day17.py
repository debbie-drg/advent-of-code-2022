import sys
from math import lcm

FILLED = "#"
EMPTY = "."


def parse_symbol(symbol: str) -> int:
    match symbol:
        case ">":
            return 1
        case "<":
            return -1
        case _:
            raise AssertionError


def parse_input(input: str) -> list[int]:
    input_list = list(input)
    input_list = list(map(parse_symbol, input_list))
    return input_list


class Rock:
    def __init__(self, shape: str, spawn_position: list[int]):
        self.rock_blocks(shape)
        self.bottom_left = spawn_position

    def rock_blocks(self, shape: str) -> None:
        match shape:
            case "-":
                self.width = 4
                self.shape = [[0, 1, 2, 3]]
            case "+":
                self.width = 3
                self.shape = [[1], [0, 1, 2], [1]]
            case "L":
                self.width = 3
                self.shape = [[0, 1, 2], [2], [2]]
            case "I":
                self.width = 1
                self.shape = [[0], [0], [0], [0]]
            case "o":
                self.width = 2
                self.shape = [[0, 1], [0, 1]]
            case _:
                raise AssertionError("Shape not found.")

    def get_positions(self) -> list[list[int]]:
        return [
            [element + self.bottom_left[1] for element in row_shape]
            for row_shape in self.shape
        ]

    def detect_colission(self, filled: list[list[int]]) -> bool:
        positions = self.get_positions()
        num_rows_to_check = min(len(filled), len(positions))
        for row in range(num_rows_to_check):
            if any(position in filled[row] for position in positions[row]):
                return True
        return False

    def side_shift(self, shift: int, filled: list[list[int]], width: int) -> None:
        if self.bottom_left[1] + self.width + shift > width:
            return None
        if self.bottom_left[1] + shift < 0:
            return None
        self.bottom_left[1] += shift
        if self.detect_colission(filled):
            self.bottom_left[1] -= shift

    def down_shift(self, filled: list[list[int]]) -> bool:
        if self.bottom_left[0] == 0:
            return True
        self.bottom_left[0] -= 1
        if self.detect_colission(filled):
            self.bottom_left[0] += 1
            return True
        return False


class RockFlow:
    def __init__(
        self,
        width: int,
        spawn_height_offset: int,
        spawn_column: int,
        moves_loop: list[int],
        shapes_loop: list[str],
    ):
        self.width = width
        self.spawn_height_offset = spawn_height_offset
        self.spawn_column = spawn_column
        self.current_height = 0
        self.filled = []
        self.moves_loop = moves_loop
        self.shapes_loop = shapes_loop
        self.move_index = 0
        self.spawn_index = 0
        self.number_spawned = 0
        self.instructions_loop = 0

    def __repr__(self):
        representation = ""
        for row in range(self.current_height - 1, -1, -1):
            representation += "|"
            for column in range(self.width):
                if column in self.filled[row]:
                    representation += FILLED
                else:
                    representation += EMPTY
            representation += "|\n"
        representation += "+" + self.width * "-" + "+\n"
        return representation

    def next_move(self) -> int:
        move = self.moves_loop[self.move_index]
        self.move_index = (self.move_index + 1) % len(self.moves_loop)
        return move

    def next_shape(self) -> str:
        shape = self.shapes_loop[self.spawn_index]
        self.spawn_index = (self.spawn_index + 1) % len(self.shapes_loop)
        return shape

    def spawn_rock(self) -> None:
        self.number_spawned += 1
        spawn_row = self.current_height + self.spawn_height_offset
        spawn_column = self.spawn_column
        current_rock = Rock(self.next_shape(), spawn_position=[spawn_row, spawn_column])
        while True:
            current_location = current_rock.bottom_left
            current_rock.side_shift(
                self.next_move(),
                filled=self.filled[current_location[0] :],
                width=self.width,
            )
            if current_rock.down_shift(self.filled[current_location[0] - 1 :]):
                break
        rock_positions = current_rock.get_positions()
        current_index = current_rock.bottom_left[0]
        for row in rock_positions:
            if current_index < self.current_height:
                self.filled[current_index] += row
            else:
                self.filled.append(row)
            current_index += 1
        self.current_height = len(self.filled)

    def spawn_many(self, number: int) -> None:
        for _ in range(number):
            self.spawn_rock()

    def spawn_and_print(self) -> None:
        self.spawn_rock()
        print(self)

    def find_loop(self):
        start_spawn_index = self.spawn_index
        start_move_index = self.move_index
        start_spawns = self.number_spawned
        while True:
            self.spawn_rock()
            if (
                start_spawn_index == self.spawn_index
                and start_move_index == self.move_index
            ):
                break
        self.instructions_loop = self.number_spawned - start_spawns

    def height_large_number(self, number_spawns: int):
        if self.instructions_loop == 0:
            self.find_loop()
        instructions_before_looping = (
            (number_spawns - self.number_spawned) % self.instructions_loop
        )
        self.spawn_many(instructions_before_looping)
        current_height = self.current_height
        self.spawn_many(self.instructions_loop)
        height_per_loop = self.current_height - current_height
        loops_remaining = (number_spawns - self.number_spawned) // self.instructions_loop
        return self.current_height + height_per_loop * loops_remaining


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    shift_symbols = open(file_name).read().strip()
    moves_loop = parse_input(shift_symbols)
    shapes_loop = ["-", "+", "L", "I", "o"]

    rock_flow = RockFlow(
        width=7,
        spawn_height_offset=3,
        spawn_column=2,
        moves_loop=moves_loop,
        shapes_loop=shapes_loop,
    )

    rock_flow.spawn_many(2022)
    print(f"The height after spawning 2022 rocks is {rock_flow.current_height}.")
    print(f"The elephants are greedy! The height at 1000000000000 spawns is {rock_flow.height_large_number(1000000000000)}.")
