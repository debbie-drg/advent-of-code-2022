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
        self.elves = []
        self.move_index = 0
        self.number_rounds = 0
        terrain_map.reverse()
        for row, line in enumerate(terrain_map):
            for column, character in enumerate(line):
                if character == "#":
                    self.elves.append(Elf((row, column)))

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
            self.top = max(self.top, elf.location[0])
            self.bottom = min(self.bottom, elf.location[0])
            self.left = min(self.left, elf.location[1])
            self.right = max(self.right, elf.location[1])

    def move_round(self) -> bool:
        self.number_rounds += 1
        locations = set([elf.location for elf in self.elves])
        trying_move = []
        for elf in self.elves:
            trying_move.append(elf.get_move(self.move_index, locations))
            if trying_move[-1]:
                elf.try_move()
        if all([trying == False for trying in trying_move]):
            return False
        self.move_index += 1
        tentative_locations = dict()
        for index, elf in enumerate(self.elves):
            if not trying_move[index]:
                continue
            try:
                tentative_locations[elf.tentative_location].append(elf)
            except KeyError:
                tentative_locations[elf.tentative_location] = [elf]
        any_moved = False
        for index, elf in enumerate(self.elves):
            if not trying_move[index]:
                continue

            if len(tentative_locations[elf.tentative_location]) == 1:
                elf.move()
                any_moved = True
        return any_moved

    def move_several(self, number_rounds: int):
        for _ in range(number_rounds):
            self.move_round()

    def rounds_until_stationary(self) -> int:
        while self.move_round():
            pass
        return self.number_rounds


class Elf:
    def __init__(self, location: tuple[int, int]):
        self.location = location

    def neighbours(self, offset: list[tuple[int, int]]) -> set[tuple[int, int]]:
        return set([tuple_sum(self.location, direction) for direction in offset])

    def get_move(self, index_offset: int, locations: set) -> bool:
        if len(locations.intersection(self.neighbours(ALL_DIRECTIONS))) == 0:
            self.move_direction = (0, 0)
            return False
        for index in range(len(NEIGHBOUR_OFFSETS)):
            move_index = (index + index_offset) % len(NEIGHBOUR_OFFSETS)
            if (
                len(
                    locations.intersection(
                        self.neighbours(NEIGHBOUR_OFFSETS[move_index])
                    )
                )
                == 0
            ):
                self.move_direction = MOVE_DIRECTIONS[move_index]
                return True
        self.move_direction = (0, 0)
        return False

    def try_move(self):
        self.tentative_location = tuple_sum(self.location, self.move_direction)

    def move(self):
        self.location = self.tentative_location


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
