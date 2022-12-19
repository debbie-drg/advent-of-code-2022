import sys
from copy import copy
import multiprocessing

TIME_LIMIT = 24
TIME_LIMIT_ELEPHANTS_NOT_HUNGRY = 32


def parse_blueprint(blueprint: str) -> tuple[int, list[list[int]]]:
    split_blueprint = blueprint.split(" ")
    blueprint_id = int(split_blueprint[1].removesuffix(":"))
    ore_robot_cost = [int(split_blueprint[6]), 0, 0, 0]
    clay_robot_cost = [int(split_blueprint[12]), 0, 0, 0]
    obsidian_robot_cost = [int(split_blueprint[18]), int(split_blueprint[21]), 0, 0]
    geode_robot_cost = [int(split_blueprint[27]), 0, int(split_blueprint[30]), 0]
    return (
        blueprint_id,
        [ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost],
    )


class Blueprint:
    def __init__(self, blueprint: str):
        self.id, self.robot_costs = parse_blueprint(blueprint)
        self.max_cost_per_resource = [
            max([robot_cost[index] for robot_cost in self.robot_costs])
            for index in range(len(self.robot_costs))
        ]
        # Ore, Clay, Obsidian, Geode.
        # Costs are codified through positions on list.

    @staticmethod
    def update_materials(materials: list[int], number_robots: list[int]) -> list[int]:
        materials_after = [
            material + number_robots
            for material, number_robots in zip(materials, number_robots)
        ]
        return materials_after

    def purchase_robot(
        self, robot_type: int, number_robots: list[int], materials: list[int]
    ) -> tuple[list[int], list[int]]:
        number_robots_after = copy(number_robots)
        number_robots_after[robot_type] += 1
        materials_after = [
            material - material_cost
            for material, material_cost in zip(materials, self.robot_costs[robot_type])
        ]
        return materials_after, number_robots_after

    def enough_materials(
        self, materials: list[int], number_robots: list[int], time_remaining: int
    ) -> list[int]:
        enough = []
        for index in range(
            len(self.robot_costs) - 1, -1, -1
        ):  # Reverse to give later robots priority
            if (
                index == 3
                or number_robots[index] * time_remaining + materials[index]
                < time_remaining * self.max_cost_per_resource[index]
            ) and all(
                [
                    material >= cost
                    for material, cost in zip(materials, self.robot_costs[index])
                ]
            ):
                enough.append(index)
        return enough

    def achievable(
        self, time_remaining: int, number_robots: list[int], materials: list[int]
    ):
        max_obsidian = (
            materials[2]
            + number_robots[2] * time_remaining
            + (time_remaining * (time_remaining - 1)) // 2
        )
        max_new_geode_robots = max_obsidian // self.robot_costs[3][2]
        achievable = materials[3] + number_robots[3] * time_remaining
        if max_new_geode_robots >= time_remaining:
            return achievable + (time_remaining * (time_remaining - 1)) // 2
        else:
            return (
                achievable
                + (max_new_geode_robots * (max_new_geode_robots - 1)) // 2
                + (time_remaining - max_new_geode_robots) * max_new_geode_robots
            )

    def next_step(
        self,
        time_remaining: int,
        materials: list[int],
        number_robots: list[int],
        max_geodes: int,
        cache: set[tuple[int]],
    ) -> tuple[int, set[tuple[int]]]:
        cache_element = tuple([time_remaining] + materials + number_robots)
        if cache_element in cache:
            return max_geodes, cache
        cache.add(cache_element)
        if self.achievable(time_remaining, number_robots, materials) <= max_geodes:
            return max_geodes, cache
        to_purchase_this_round = self.enough_materials(
            materials, number_robots, time_remaining
        )
        materials = self.update_materials(materials, number_robots)
        if time_remaining == 1:
            return materials[3], cache
        geodes, cache = self.next_step(
            time_remaining - 1, materials, number_robots, max_geodes, cache
        )
        max_geodes = max(max_geodes, geodes)
        # If no purchase
        for (
            robot_type
        ) in (
            to_purchase_this_round
        ):  # For the possible purchases. Later robots are purchased first.
            geodes, cache = self.next_step(
                time_remaining - 1,
                *self.purchase_robot(robot_type, number_robots, materials),
                max_geodes,
                cache,
            )
            max_geodes = max(geodes, max_geodes)
        return max_geodes, cache

    def max_geodes(self, time_limit: int) -> int:
        number_robots = [1, 0, 0, 0]
        materials = [0, 0, 0, 0]
        cache = set()
        max_geodes, _ = self.next_step(time_limit, materials, number_robots, 0, cache)
        return max_geodes

    def quality_level(self, time_limit: int) -> int:
        return self.max_geodes(time_limit) * self.id


def quality_level(blueprint: Blueprint) -> int:
    global TIME_LIMIT
    return blueprint.quality_level(TIME_LIMIT)


def max_geodes(blueprint: Blueprint) -> int:
    global TIME_LIMIT_ELEPHANTS_NOT_HUNGRY
    return blueprint.max_geodes(TIME_LIMIT_ELEPHANTS_NOT_HUNGRY)


def multiprocess_quality_levels(blueprints: list[Blueprint]):
    with multiprocessing.Pool() as pool:
        results = 0
        for result in pool.map(quality_level, blueprints):
            results += result
    return results


def multiprocess_max_geodes(blueprints: list[Blueprint]):
    with multiprocessing.Pool() as pool:
        results = 1
        for result in pool.map(max_geodes, blueprints):
            results *= result
    return results


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    blueprints = open(file_name).read().split("\n")
    try:
        blueprints.remove("")
    except ValueError:
        pass

    blueprints = list(map(Blueprint, blueprints))

    print(f"The total quality level is {multiprocess_quality_levels(blueprints)}.")
    print(
        f"The first three blueprints produce a product of {multiprocess_max_geodes(blueprints[:3])}."
    )
