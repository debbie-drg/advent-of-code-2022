import sys

NEIGHBOURS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


def sum_tuple(tuple_1: tuple[int, int], tuple_2: tuple[int, int]) -> tuple[int, int]:
    return (tuple_1[0] + tuple_2[0], tuple_1[1] + tuple_2[1])


class Basin:
    def __init__(self, basin_input: str) -> None:
        split_basin_input = basin_input.splitlines()
        self.blizzards = []
        self.blizzard_locations = set()
        self.lower_vertical = 0
        self.upper_vertical = len(split_basin_input) - 1
        self.lower_horizontal = 0
        self.upper_horizontal = len(split_basin_input[0]) - 1
        self.start_point = (0, 1)
        self.end_point = (self.upper_vertical, self.upper_horizontal - 1)
        for row_index, row in enumerate(split_basin_input):
            for column_index, character in enumerate(row):
                if character == ">":
                    self.blizzards.append(
                        Blizzard(
                            (row_index, column_index),
                            (0, 1),
                            (row_index, self.lower_horizontal),
                            (row_index, self.upper_horizontal),
                        )
                    )
                if character == "<":
                    self.blizzards.append(
                        Blizzard(
                            (row_index, column_index),
                            (0, -1),
                            (row_index, self.upper_horizontal),
                            (row_index, self.lower_horizontal),
                        )
                    )
                if character == "^":
                    self.blizzards.append(
                        Blizzard(
                            (row_index, column_index),
                            (-1, 0),
                            (self.upper_vertical, column_index),
                            (self.lower_vertical, column_index),
                        )
                    )
                if character == "v":
                    self.blizzards.append(
                        Blizzard(
                            (row_index, column_index),
                            (1, 0),
                            (self.lower_vertical, column_index),
                            (self.upper_vertical, column_index),
                        )
                    )

    def update_blizzards(self) -> None:
        blizard_locations = set()
        for blizzard in self.blizzards:
            blizzard.move()
            blizard_locations.add(blizzard.location)
        self.blizzard_locations = blizard_locations

    def next_possible_steps(self, location: tuple[int, int]) -> set[tuple[int, int]]:
        move_options = [sum_tuple(location, neighbour) for neighbour in NEIGHBOURS]
        return {
            location
            for location in move_options
            if location not in self.blizzard_locations
            and (
                location in [self.start_point, self.end_point]
                or (
                    (self.lower_horizontal < location[1] < self.upper_horizontal)
                    and (self.lower_vertical < location[0] < self.upper_vertical)
                )
            )
        }

    def find_path(self, reverse=False) -> int:
        locations = {self.start_point} if not reverse else {self.end_point}
        time_elapsed = 0
        while True:
            self.update_blizzards()
            time_elapsed += 1
            next_round_locations = set()
            for location in locations:
                next_round_locations = next_round_locations.union(
                    self.next_possible_steps(location)
                )
            if self.end_point in next_round_locations and not reverse:
                return time_elapsed
            if self.start_point in next_round_locations and reverse:
                return time_elapsed
            locations = next_round_locations


class Blizzard:
    def __init__(
        self,
        location: tuple[int, int],
        move_direction: tuple[int, int],
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> None:
        self.location = location
        self.move_direction = move_direction
        self.start = start
        self.end = end

    def move(self) -> None:
        self.location = sum_tuple(self.location, self.move_direction)
        if self.location == self.end:
            self.location = sum_tuple(self.start, self.move_direction)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    blizzard_basin = Basin(open(file_name).read())

    first_time_going = blizzard_basin.find_path()

    print(f"You can get to the exit in {first_time_going} minutes.")

    going_back = blizzard_basin.find_path(reverse=True)
    going_again = blizzard_basin.find_path()

    print(
        f"You can go, go back and fetch the snacks and go again in {first_time_going + going_back + going_again} minutes."
    )
