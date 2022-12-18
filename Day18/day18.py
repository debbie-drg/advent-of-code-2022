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


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"

    cubes_input = open(file_name).read()
    lava = Lava(cubes_input)

    print(f"The surface area is {lava.surface_area()}.")
