import sys

ORD_MIN = ord("a")
ORD_MAX = ord("z")
ALTITUDE_DICT = {"S": 0, "E": ORD_MAX - ORD_MIN}
for element in "abcdefghijklmnopqrstuvwxyz":
    ALTITUDE_DICT[element] = ord(element) - ORD_MIN


def row_col_to_pos(row: int, column: int, number_rows: int, number_columns: int) -> int:
    return row * number_columns + column


def pos_to_col_and_row(position: int, number_rows: int, number_columns: int) -> int:
    row = position // number_columns
    column = position % number_columns
    return (row, column)


def check_neighbours(
    elevation_map: str, position: int, number_rows: int, number_cols: int
) -> list[list[int]]:
    neighbours = []
    current_altitude = ALTITUDE_DICT[elevation_map[position]]
    number_elements = number_rows * number_cols
    row, column = pos_to_col_and_row(position, number_rows, number_cols)

    top = row_col_to_pos(row - 1, column, number_rows, number_cols)
    if top >= 0 and ALTITUDE_DICT[elevation_map[top]] >= current_altitude - 1:
        neighbours.append(top)

    left = position - 1
    if left >= 0 and ALTITUDE_DICT[elevation_map[left]] >= current_altitude - 1:
        neighbours.append(left)

    bottom = row_col_to_pos(row + 1, column, number_rows, number_cols)
    if (
        bottom < number_elements
        and ALTITUDE_DICT[elevation_map[bottom]] >= current_altitude - 1
    ):
        neighbours.append(bottom)

    right = position + 1
    if (
        right < number_elements
        and ALTITUDE_DICT[elevation_map[right]] >= current_altitude - 1
    ):
        neighbours.append(right)

    return neighbours


class Terrain:
    def __init__(self, elevation_map: str):
        global ALTITUDE_DICT
        split_map = elevation_map.split("\n")
        split_map.remove("")
        self.distances_computed = False
        self.number_rows = len(split_map)
        self.number_cols = len(split_map[0])
        elevation_map = elevation_map.replace("\n", "")
        self.positions = []
        number_elements = len(elevation_map)

        for index, element in enumerate(elevation_map):
            self.positions.append(
                Position(ALTITUDE_DICT[element], index, number_elements)
            )
            if element == "S":
                self.start = index
            if element == "E":
                self.end = index
                self.positions[-1].distance_to_end = 0
            self.positions[-1].neighbours = check_neighbours(
                elevation_map, index, self.number_rows, self.number_cols
            )

    def compute_distances(self):
        self.distances_computed = True
        unvisited = list(range(len(self.positions)))
        current_position = self.end
        max_distance = self.positions[self.start].distance_to_end
        while unvisited != []:
            if current_position == self.start:
                break
            tentative_distance = self.positions[current_position].distance_to_end + 1
            for neighbour in [
                neighbour
                for neighbour in self.positions[current_position].neighbours
                if neighbour in unvisited
            ]:
                if tentative_distance < self.positions[neighbour].distance_to_end:
                    self.positions[neighbour].distance_to_end = tentative_distance
            unvisited.remove(current_position)
            min_unvisited_distance = max_distance
            for position in unvisited:
                if self.positions[position].distance_to_end <= min_unvisited_distance:
                    current_position = position
                    min_unvisited_distance = self.positions[position].distance_to_end

    def distance(self):
        if not self.distances_computed:
            self.compute_distances()
        return self.positions[self.start].distance_to_end

    def min_distance_from_bottom(self) -> int:
        if not self.distances_computed:
            self.compute_distances()
        distance = self.number_rows * self.number_cols
        for position in self.positions:
            if position.altitude == 0:
                distance = min(distance, position.distance_to_end)
        return distance


class Position:
    def __init__(self, altitude: int, position: int, distance_to_end: int):
        self.altitude = altitude
        self.neighbours = []
        self.position = position
        self.distance_to_end = distance_to_end

    def __repr__(self):
        return f"Position at {self.position} of altitude {self.altitude}."


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    elevation_map = open(file_name).read()
    terrain_map = Terrain(elevation_map)

    print(f"The shortest path has length {terrain_map.distance()}.")
    print(
        f"The closest point from the botton is at {terrain_map.min_distance_from_bottom()} steps from the end."
    )
