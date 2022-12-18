import sys


def parse_one_cube(cube: str) -> tuple[int]:
    split_cube = cube.split(",")
    return tuple(map(int, split_cube))


def number_neighbours(cube: tuple, other_cubes: list[tuple]):
    neighbours = 0
    if (cube[0] - 1, cube[1], cube[2]) in other_cubes:
        neighbours += 1
    if (cube[0] + 1, cube[1], cube[2]) in other_cubes:
        neighbours += 1
    if (cube[0], cube[1] - 1, cube[2]) in other_cubes:
        neighbours += 1
    if (cube[0], cube[1] + 1, cube[2]) in other_cubes:
        neighbours += 1
    if (cube[0], cube[1], cube[2] - 1) in other_cubes:
        neighbours += 1
    if (cube[0], cube[1], cube[2] + 1) in other_cubes:
        neighbours += 1
    return neighbours


def surface_area(cubes_list: list[tuple]) -> int:
    surface_area = 6 * len(cubes_list)
    for index in range(len(cubes_list) - 1):
        surface_area -= 2 * number_neighbours(cubes_list[index], cubes_list[index + 1:])
    return surface_area


def parse_cubes(cubes_input: str) -> list[tuple[int]]:
    split_cubes = cubes_input.split("\n")
    try:
        split_cubes.remove("")
    except ValueError:
        pass
    return list(map(parse_one_cube, split_cubes))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    cubes = parse_cubes(open(file_name).read())

    print(f"The surface area is {surface_area(cubes)}.")
