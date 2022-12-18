import sys

NEIGHBOURS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


class Lava:
    def __init__(self, cubes_input: str):
        self.cubes = []
        split_cubes = cubes_input.split("\n")
        try:
            split_cubes.remove("")
        except ValueError:
            pass
        for cube in split_cubes:
            self.add_cube(cube)
        max_indices = (max(cube[i] for cube in self.cubes) for i in range(3))
        min_indices = (min(cube[i] for cube in self.cubes) for i in range(3))
        self.max_x, self.max_y, self.max_z = max_indices
        self.min_x, self.min_y, self.min_z = min_indices

    def add_cube(self, cube: str):
        split_cube = cube.split(",")
        self.cubes.append(tuple(map(int, split_cube)))

    def number_neighbours(self, cube: tuple) -> int:
        neighbours = 0
        for neighbour in NEIGHBOURS:
            if (
                cube[0] + neighbour[0],
                cube[1] + neighbour[1],
                cube[2] + neighbour[2],
            ) in self.cubes:
                neighbours += 1
        return neighbours

    def surface_area(self) -> int:
        surface_area = 6 * len(self.cubes)
        for cube in self.cubes:
            surface_area -= self.number_neighbours(cube)
        return surface_area

    def out_of_bounds(self, position):
        upper_check = any(
            [
                position[0] > self.max_x + 1,
                position[1] > self.max_y + 1,
                position[2] > self.max_z + 1,
            ]
        )
        lower_check = any(
            [
                position[0] < self.min_x - 1,
                position[1] < self.min_y - 1,
                position[2] < self.min_z - 1,
            ]
        )
        return upper_check or lower_check

    def outer_surface(self) -> int:
        checked = []
        to_check = [(self.min_x - 1, self.min_y - 1, self.min_z - 1)]
        surface = 0
        while to_check != []:
            position = to_check.pop()
            if position in checked:
                continue
            for neighbour in NEIGHBOURS:
                next_step = (
                    position[0] + neighbour[0],
                    position[1] + neighbour[1],
                    position[2] + neighbour[2],
                )
                if self.out_of_bounds(next_step):
                    continue
                if next_step in checked:
                    continue
                if next_step in self.cubes:
                    surface += 1
                    continue
                to_check.append(next_step)
            checked.append(position)
        return surface


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"

    cubes_input = open(file_name).read()
    lava = Lava(cubes_input)

    print(f"The surface area is {lava.surface_area()}.")
    print(f"The outer surface area is {lava.outer_surface()}.")
