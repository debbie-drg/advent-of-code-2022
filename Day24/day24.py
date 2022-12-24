import sys


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
        for row_index, row in enumerate(split_basin_input[1:-1]):
            for column_index, character in enumerate(row[1:-1]):
                if character == ">":
                    self.blizzards.append(
                        Blizzard(
                            (row_index + 1, column_index + 1),
                            (0, 1),
                            (row_index + 1, self.lower_horizontal),
                            (row_index + 1, self.upper_horizontal),
                        )
                    )
                    self.blizzard_locations.add((row_index + 1, column_index + 1))
                if character == "<":
                    self.blizzards.append(
                        Blizzard(
                            (row_index + 1, column_index + 1),
                            (0, -1),
                            (row_index + 1, self.upper_horizontal),
                            (row_index + 1, self.lower_horizontal),
                        )
                    )
                    self.blizzard_locations.add((row_index + 1, column_index + 1))
                if character == "^":
                    self.blizzards.append(
                        Blizzard(
                            (row_index + 1, column_index + 1),
                            (-1, 0),
                            (self.upper_vertical, column_index + 1),
                            (self.lower_vertical, column_index + 1),
                        )
                    )
                    self.blizzard_locations.add((row_index + 1, column_index + 1))
                if character == "v":
                    self.blizzards.append(
                        Blizzard(
                            (row_index + 1, column_index + 1),
                            (1, 0),
                            (self.lower_vertical, column_index + 1),
                            (self.upper_vertical, column_index + 1),
                        )
                    )
                    self.blizzard_locations.add((row_index + 1, column_index + 1))

    def __repr__(self) -> str:
        representation = "#" * (self.upper_horizontal + 1) + "\n"
        for row_index in range(1, self.upper_vertical):
            representation += "#"
            for col_index in range(1, self.upper_horizontal):
                if (row_index, col_index) in self.blizzard_locations:
                    representation += "#"
                else:
                    representation += "."
            representation += "#\n"
        representation += "#" * (self.upper_horizontal + 1)
        return representation

    def update_blizzards(self) -> None:
        blizard_locations = set()
        for blizzard in self.blizzards:
            blizzard.move()
            blizard_locations.add(blizzard.location)
        self.blizzard_locations = blizard_locations

    def neighbours(self, location: tuple[int, int]) -> set[tuple[int, int]]:
        neighbours = set([location])
        if location == self.start_point:
            neighbours.add((1, 1))
            return neighbours
        if location == self.end_point:
            neighbours.add((self.upper_vertical - 1, self.upper_horizontal - 1))
            return neighbours
        if location[0] - 1 != self.lower_vertical or location[1] == self.start_point[1]:
            neighbours.add(sum_tuple((-1, 0), location))
        if location[0] + 1 != self.upper_vertical or location[1] == self.end_point[1]:
            neighbours.add(sum_tuple((1, 0), location))
        if location[1] - 1 != self.lower_horizontal:
            neighbours.add(sum_tuple((0, -1), location))
        if location[1] + 1 != self.upper_horizontal:
            neighbours.add(sum_tuple((0, 1), location))
        return neighbours

    def get_next_possible_steps(
        self, location: tuple[int, int]
    ) -> list[tuple[int, int]]:
        next_possible_locations = self.neighbours(location)
        return [
            neighbour
            for neighbour in next_possible_locations
            if neighbour not in self.blizzard_locations
        ]

    def find_path(self, reverse=False) -> int:
        locations = set([self.start_point]) if not reverse else set([self.end_point])
        time_elapsed = 0
        while True:
            self.update_blizzards()
            time_elapsed += 1
            next_round_locations = set()
            for location in locations:
                next_round_locations = next_round_locations.union(
                    self.get_next_possible_steps(location)
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
