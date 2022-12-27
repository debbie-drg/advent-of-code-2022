import sys

DIRECTION_VALUES = [(1, 0), (0, 1), (-1, 0), (0, -1)]
# Right, down, left, up
# Anlges are 0, 1 (90), 2 (180), 3 (270)

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


def sum_tuples(tuple_1: tuple[int, int], tuple_2: tuple[int, int]) -> tuple[int, int]:
    return (tuple_1[0] + tuple_2[0], tuple_1[1] + tuple_2[1])


def substract_tuples(
    tuple_1: tuple[int, int], tuple_2: tuple[int, int]
) -> tuple[int, int]:
    return (tuple_1[0] - tuple_2[0], tuple_1[1] - tuple_2[1])


def scalar_times_tuple(scalar: int, in_tuple: tuple[int, int]) -> tuple[int, int]:
    return (scalar * in_tuple[0], scalar * in_tuple[1])


class JungleFace:
    def __init__(self, top_right: tuple[int, int], walls: set[tuple[int, int]]):
        self.walls = walls
        self.top_right = top_right

    def in_map_position(self, location: tuple[int, int]):
        return sum_tuples(location, self.top_right)

    def is_wall(self, location: tuple[int, int]) -> bool:
        return location in self.walls


class JungleCube:
    def __init__(self, terrain: list[str], cube_configuration: bool = False):
        self.faces = []
        self.cube_corners = self.get_top_left(terrain)
        assert len(self.cube_corners) == 6, "Input does not seem to be a cube"
        for corner in self.cube_corners:
            self.faces.append(JungleFace(corner, self.get_walls(terrain, corner)))
        self.set_cube_configuration(cube_configuration)

    @staticmethod
    def compute_cube_size(terrain: list[str]) -> int:
        positions_count = 0
        for line in terrain:
            positions_count += len(line.strip())
        return int((positions_count // 6) ** (1 / 2))

    def get_top_left(self, terrain: list[str]) -> list[tuple[int, int]]:
        self.cube_size = self.compute_cube_size(terrain)
        square_corners = []
        for vertical_index in range(0, len(terrain), self.cube_size):
            for horizontal_index in range(
                0, len(terrain[vertical_index]), self.cube_size
            ):
                if terrain[vertical_index][horizontal_index] != " ":
                    square_corners.append((horizontal_index, vertical_index))
        return square_corners

    def get_walls(
        self, terrain: list[str], top_left: tuple[int, int]
    ) -> set[tuple[int, int]]:
        walls = set()
        for vertical_index in range(top_left[0], top_left[0] + self.cube_size):
            for horizontal_index in range(top_left[1], top_left[1] + self.cube_size):
                if terrain[horizontal_index][vertical_index] == "#":
                    walls.add(
                        substract_tuples((vertical_index, horizontal_index), top_left)
                    )
        return walls

    def set_cube_configuration(self, cube_mode: bool):
        self.restart_configuration()
        for index, corner in enumerate(self.cube_corners):
            for direction_index, direction in enumerate(DIRECTION_VALUES):
                current_tuple = sum_tuples(
                    corner, scalar_times_tuple(self.cube_size, direction)
                )
                if current_tuple in self.cube_corners:
                    self.faces[index].neighbours[
                        direction_index
                    ] = self.cube_corners.index(current_tuple)
        if not cube_mode:
            self.set_cube_wrapping()
        self.fold_cube()

    def set_cube_wrapping(self):
        for index in range(len(self.cube_corners)):
            for direction_index in range(len(DIRECTION_VALUES)):
                if self.faces[index].neighbours[direction_index] != -1:
                    continue
                opposite_direction = (direction_index + 2) % len(DIRECTION_VALUES)
                current_index = index
                next_index = self.faces[index].neighbours[opposite_direction]
                while next_index not in [-1, index]:
                    current_index = next_index
                    next_index = self.faces[current_index].neighbours[opposite_direction]
                self.faces[index].neighbours[direction_index] = current_index
                    
    def fold_cube(self):
        pass

    def restart_configuration(self):
        self.current_face = 0
        self.position = (0, 0)
        self.direction_index = 0
        for face in self.faces:
            face.neighbours = [-1, -1, -1, -1]
            face.neighbour_angles = [0, 0, 0, 0]

    def wrap_location(
        self, current_location: tuple[int, int], angle: int
    ) -> tuple[int, int]:
        last_coordinate = self.cube_size - 1
        if self.direction_index == 0:
            if angle == 0:
                return (0, current_location[1])
            if angle == 1:
                return (last_coordinate - current_location[1], 0)
            if angle == 2:
                return (last_coordinate, last_coordinate - current_location[1])
            if angle == 3:
                return (0, current_location[1])
        if self.direction_index == 1:
            if angle == 0:
                return (current_location[0], 0)
            if angle == 1:
                return (last_coordinate, current_location[0])
            if angle == 2:
                return (last_coordinate - current_location[0], last_coordinate)
            if angle == 3:
                return (0, current_location[0])
        if self.direction_index == 2:
            if angle == 0:
                return (last_coordinate, current_location[1])
            if angle == 1:
                return (last_coordinate - current_location[1], last_coordinate)
            if angle == 2:
                return (last_coordinate, last_coordinate - current_location[1])
            if angle == 3:
                return (current_location[1], 0)
        if self.direction_index == 3:
            if angle == 0:
                return (current_location[0], last_coordinate)
            if angle == 1:
                return (0, current_location[0])
            if angle == 2:
                return (last_coordinate - current_location[0], last_coordinate)
            if angle == 3:
                return (last_coordinate, last_coordinate - current_location[0])
        raise AssertionError

    def is_out_of_bounds(self, position: tuple[int, int]) -> bool:
        return any([element < 0 or element >= self.cube_size for element in position])

    def move(self, number_moves: int):
        direction = DIRECTION_VALUES[self.direction_index]
        for _ in range(number_moves):
            next_position = sum_tuples(self.position, direction)
            if self.is_out_of_bounds(next_position):
                angle = self.faces[self.current_face].neighbour_angles[
                        self.direction_index
                    ]
                next_position = self.wrap_location(
                    self.position,
                    angle,
                )
                next_face = self.faces[self.current_face].neighbours[
                    self.direction_index
                ]
                if self.faces[next_face].is_wall(next_position):
                    return None
                self.position = next_position
                self.current_face = next_face
                self.direction_index += angle
                self.direction_index %= len(DIRECTION_VALUES)
                direction = DIRECTION_VALUES[self.direction_index]
            else:
                if self.faces[self.current_face].is_wall(next_position):
                    return None
                self.position = next_position

    def in_map_location(self) -> tuple[int,int]:
        return self.faces[self.current_face].in_map_position(self.position)

    def password(self) -> int:
        position = self.in_map_location()
        return (
            1000 * (position[1] + 1)
            + 4 * (position[0] + 1)
            + self.direction_index
        )

    def path_move(self, instructions):
        self.direction_index = 0
        for instruction in instructions:
            if isinstance(instruction, int):
                self.move(instruction)
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

    jungle = JungleCube(terrain)
    instructions = parse_instructions(moves)
    jungle.path_move(instructions)
    print(f"The password is {jungle.password()}.")

    jungle.set_cube_configuration(True)
    jungle.path_move(instructions)
    print(f"The password when seen as cube is {jungle.password()}.")
