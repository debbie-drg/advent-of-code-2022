import sys

ROCK_CHARACTER = "██"
EMPTY_CHARACTER = "  "
SAND_CHARACTER = "░░"


class Reservoir:
    def __init__(self, rock_traces: list[str]):
        self.filled_positions = {}
        self.sand_source = (500, 0)
        rock_lines = preprocess_input(rock_traces)
        for rock_line in rock_lines:
            for index in range(len(rock_line)):
                self.add_rock(rock_line[index])
                if index > 0:
                    self.add_line(rock_line[index - 1], rock_line[index])
        self.find_extremes()

    def __repr__(self):
        representation = ""
        for ver_index in range(self.top, self.bottom + 1):
            for hor_index in range(self.left, self.right + 1):
                if (hor_index, ver_index) in self.filled_positions:
                    match self.filled_positions[(hor_index, ver_index)]:
                        case "rock":
                            representation += ROCK_CHARACTER
                        case "sand":
                            representation += SAND_CHARACTER
                else:
                    representation += EMPTY_CHARACTER
            representation += "\n"
        return representation

    def add_sand_grain(self, line_added: bool = False) -> bool:
        sand_position = self.sand_source
        while True:
            if line_added and sand_position[1] == self.bottom - 1:
                self.add_rock((sand_position[0], self.bottom), check=True)
                self.add_rock((sand_position[0] - 1, self.bottom), check=True)
                self.add_rock((sand_position[0] + 1, self.bottom), check=True)
                self.add_sand(sand_position)
                return False
            if sand_position[1] == self.bottom:
                return True
            if (sand_position[0], sand_position[1] + 1) not in self.filled_positions:
                sand_position = (sand_position[0], sand_position[1] + 1)
            elif (
                sand_position[0] - 1,
                sand_position[1] + 1,
            ) not in self.filled_positions:
                sand_position = (sand_position[0] - 1, sand_position[1] + 1)
            elif (
                sand_position[0] + 1,
                sand_position[1] + 1,
            ) not in self.filled_positions:
                sand_position = (sand_position[0] + 1, sand_position[1] + 1)
            else:
                self.add_sand(sand_position)
                return sand_position == self.sand_source


    def add_floor_line(self):
        for index in range(self.left, self.right + 1):
            self.add_rock((index, self.bottom + 2))
        self.bottom = self.bottom + 2

    def find_extremes(self):
        self.bottom = 0
        self.top = 0
        self.left = 500
        self.right = 500
        for rock in [
            position
            for position in self.filled_positions
            if self.filled_positions[position] == "rock"
        ]:
            left, right = rock[0], rock[1]
            self.bottom = max(self.bottom, right)
            self.top = min(self.top, right)
            self.left = min(self.left, left)
            self.right = max(self.right, left)

    def add_rock(self, rock_pos: tuple[int], check: bool = False):
        if check:
            if rock_pos in self.filled_positions:
                return None
            else:
                self.left = min(self.left, rock_pos[0])
                self.right = max(self.right, rock_pos[0])
        self.filled_positions[rock_pos] = "rock"

    def add_sand(self, sand_pos: list):
        self.filled_positions[sand_pos] = "sand"

    def add_line(self, rock_1, rock_2):
        if (rock_1[0] == rock_2[0]) == (rock_1[1] == rock_2[1]):
            return None
        if rock_1[0] != rock_2[0]:
            right = rock_1[1]
            min_left = min(rock_1[0], rock_2[0])
            max_left = max(rock_1[0], rock_2[0])
            for left in range(min_left + 1, max_left):
                self.add_rock((left, right))
            return None
        left = rock_1[0]
        min_right = min(rock_1[1], rock_2[1])
        max_right = max(rock_1[1], rock_2[1])
        for right in range(min_right + 1, max_right):
            self.add_rock((left, right))
        return None


def preprocess_input(rock_traces: str) -> list[list[list[int]]]:
    rock_positions = []
    for rock_line in rock_traces:
        rock_line = rock_line.replace("->", "")
        rock_line = rock_line.split("  ")
        rock_line = [position.split(",") for position in rock_line]
        rock_line = [(int(position[0]), int(position[1])) for position in rock_line]
        rock_positions.append(rock_line)
    return rock_positions


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    rock_traces = open(file_name).read().split("\n")
    rock_traces.remove("")
    reservoir = Reservoir(rock_traces)
    index = 0
    while True:
        if reservoir.add_sand_grain():
            break
        index += 1
    print(f"Last sitting grain of sand after {index} time units.")
    reservoir.add_floor_line()
    while True:
        index += 1
        if reservoir.add_sand_grain(line_added=True):
            break
    print(f"Sand blocks the source after {index} units of time.")
