import sys

FILLED = "#"
EMPTY = "."


def parse_symbol(symbol: str):
    match symbol:
        case ">":
            return 1
        case "<":
            return -1
        case _:
            raise AssertionError


def parse_input(input):
    input = list(input)
    input = list(map(parse_symbol, input))
    return input


class Rock:
    def __init__(self, shape, spawn_position):
        self.rock_blocks(shape)
        self.bottom_left = spawn_position

    def rock_blocks(self, shape):
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

    def shift(self, shift):
        self.bottom_left[0] += shift[0]
        self.bottom_left[1] += shift[1]

    def get_positions(self):
        return [
            [element + self.bottom_left[1] for element in row_shape]
            for row_shape in self.shape
        ]

    def detect_colission(self, filled):
        positions = self.get_positions()
        num_rows_to_check = min(len(filled), len(positions))
        for row in range(num_rows_to_check):
            if any(position in filled[row] for position in positions[row]):
                return True
        return False

    def side_shift(self, shift, filled, width):
        if self.bottom_left[1] + self.width + shift > width:
            return None
        if self.bottom_left[1] + shift < 0:
            return None
        self.bottom_left[1] += shift
        if self.detect_colission(filled):
            self.bottom_left[1] -= shift

    def down_shift(self, filled):
        if self.bottom_left[0] == 0:
            return True
        self.bottom_left[0] -= 1
        if self.detect_colission(filled):
            self.bottom_left[0] += 1
            return True
        return False


class RockFlow:
    def __init__(
        self, width, spawn_height_offset, spawn_column, moves_loop, shapes_loop
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

    def next_move(self):
        move = self.moves_loop[self.move_index]
        self.move_index = (self.move_index + 1) % len(self.moves_loop)
        return move

    def next_shape(self):
        shape = self.shapes_loop[self.spawn_index]
        self.spawn_index = (self.spawn_index + 1) % len(self.shapes_loop)
        return shape

    def spawn_rock(self):
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

    def spawn_many(self, number):
        for _ in range(number):
            self.spawn_rock()

    def spawn_and_print(self):
        self.spawn_rock()
        print(self)


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
