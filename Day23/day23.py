import sys

NEIGHBOUR_OFFSETS = [
    [(1, 0), (1, 1), (1, -1)],  # N, NE, NW
    [(-1, 0), (-1, 1), (-1, -1)],  # S, SE, SW
    [(0, -1), (-1, -1), (1, -1)],  # W, NW, SW
    [(0, 1), (1, 1), (-1, 1)],  # E, NE, SW
]
MOVE_DIRECTIONS = [(1, 0), (-1, 0), (0, -1), (0, 1)]
ALL_DIRECTIONS = [(0, 1), (1, 1), (-1, 1), (0, -1), (1, -1), (-1, -1), (-1, 0), (1, 0)]


def tuple_sum(tuple_1: tuple[int, int], tuple_2: tuple[int, int]) -> tuple[int, int]:
    return (tuple_1[0] + tuple_2[0], tuple_1[1] + tuple_2[1])


class ElfGroove:
    def __init__(self, terrain_map: list[str]):
        self.elves = set()
        self.move_index = 0
        self.number_rounds = 0
        terrain_map.reverse()
        for row, line in enumerate(terrain_map):
            for column, character in enumerate(line):
                if character == "#":
                    self.elves.add((row, column))

    def __repr__(self) -> str:
        self.get_boundaries()
        locations = [elf.location for elf in self.elves]
        representation = ""
        for row in range(self.top, self.bottom - 1, -1):
            for column in range(self.left, self.right + 1):
                if (row, column) in locations:
                    representation += "#"
                else:
                    representation += "."
            representation += "\n"
        return representation

    def count_empty(self) -> int:
        self.get_boundaries()
        total_locations = (self.top - self.bottom + 1) * (self.right - self.left + 1)
        return total_locations - len(self.elves)

    def get_boundaries(self):
        self.top, self.bottom, self.left, self.right = 0, 0, 0, 0
        for elf in self.elves:
            self.top = max(self.top, elf[0])
            self.bottom = min(self.bottom, elf[0])
            self.left = min(self.left, elf[1])
            self.right = max(self.right, elf[1])

    @staticmethod
    def neighbours(
        location: tuple[int, int], offset: list[tuple[int, int]]
    ) -> set[tuple[int, int]]:
        return set(map(lambda x: tuple_sum(location, x), offset))

    def get_tentative_move(self, location) -> tuple[int, int]:
        if len(self.elves.intersection(self.neighbours(location, ALL_DIRECTIONS))) == 0:
            return location
        for index in range(len(NEIGHBOUR_OFFSETS)):
            move_index = (index + self.move_index) % len(NEIGHBOUR_OFFSETS)
            if (
                len(
                    self.elves.intersection(
                        self.neighbours(location, NEIGHBOUR_OFFSETS[move_index])
                    )
                )
                == 0
            ):
                return tuple_sum(MOVE_DIRECTIONS[move_index], location)
        return location

    def move_round(self) -> bool:
        self.number_rounds += 1
        tentative_locations = dict()
        new_locations = set()
        any_moved = False
        for elf in self.elves:
            tentative_position = self.get_tentative_move(elf)
            if tentative_position != elf:
                any_moved = True
                try:
                    tentative_locations[tentative_position].append(elf)
                except KeyError:
                    tentative_locations[tentative_position] = [elf]
            else:
                new_locations.add(elf)
        if not any_moved:
            return False
        self.move_index += 1
        any_moved = False
        for position in tentative_locations:
            if len(tentative_locations[position]) == 1:
                new_locations.add(position)
                any_moved = True
            else:
                for elf in tentative_locations[position]:
                    new_locations.add(elf)
        self.elves = new_locations
        return any_moved

    def move_several(self, number_rounds: int):
        for _ in range(number_rounds):
            self.move_round()

    def rounds_until_stationary(self) -> int:
        while self.move_round():
            pass
        return self.number_rounds


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().splitlines()

    elf_groove = ElfGroove(input_data)

    elf_groove.move_several(10)
    print(f"The number of empty tiles is {elf_groove.count_empty()}.")
    print(
        f"The number of move rounds until stationary is {elf_groove.rounds_until_stationary()}."
    )
