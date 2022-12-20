import sys
from copy import copy
import multiprocessing
from math import ceil

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
    def update_materials(
        materials: list[int], number_robots: list[int], number_turns: int
    ) -> list[int]:
        materials_after = [
            material + number_turns * number_robots
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

    def turns_to_purchase(
        self,
        materials: list[int],
        number_robots: list[int],
        time_remaining: int,
        robot_type: int,
    ) -> int:
        if robot_type != 3 and (
            number_robots[robot_type] * time_remaining + materials[robot_type]
            >= time_remaining * self.max_cost_per_resource[robot_type]
        ):
            return -1  # Purchasing would be useless
        turns_to_wait = 0
        for material, cost, robots in zip(
            materials, self.robot_costs[robot_type], number_robots
        ):
            if cost == 0 or material >= cost:
                continue
            if robots == 0:
                return -1  # Cannot get enough materials by waiting
            turns_to_wait = max(turns_to_wait, ceil((cost - material) / robots))
        if turns_to_wait < time_remaining - 1:
            return turns_to_wait
        return -1  # Time to purchase longer than time remaining

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
        robot_to_build: int | None,
        max_geodes: int,
        cache: set[tuple[int]],
    ) -> tuple[int, set[tuple[int]]]:

        if robot_to_build is not None:
            time_remaining -= 1
            materials = self.update_materials(materials, number_robots, 1)
            materials, number_robots = self.purchase_robot(
                robot_to_build, number_robots, materials
            )

        if self.achievable(time_remaining, number_robots, materials) <= max_geodes:
            return max_geodes, cache

        cache_element = tuple([time_remaining] + materials + number_robots)
        if cache_element in cache:
            return max_geodes, cache
        cache.add(cache_element)

        for robot_type in range(len(materials) - 1, -1, -1):
            time_to_wait = self.turns_to_purchase(
                materials, number_robots, time_remaining, robot_type
            )
            if time_to_wait == -1:
                continue
            geodes, cache = self.next_step(
                time_remaining - time_to_wait,
                self.update_materials(materials, number_robots, time_to_wait),
                copy(number_robots),
                robot_type,
                max_geodes,
                cache,
            )
            max_geodes = max(geodes, max_geodes)

        # We do not purchase until the end
        geodes = materials[3] + number_robots[3] * time_remaining
        max_geodes = max(geodes, max_geodes)
        return max_geodes, cache

    def max_geodes(self, time_limit: int) -> int:
        number_robots = [1, 0, 0, 0]
        materials = [0, 0, 0, 0]
        cache = set()
        max_geodes, _ = self.next_step(
            time_limit, materials, number_robots, None, 0, cache
        )
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
    blueprints = open(file_name).read().splitlines()
    blueprints = list(map(Blueprint, blueprints))

    print(f"The total quality level is {multiprocess_quality_levels(blueprints)}.")
    print(
        f"The first three blueprints produce a product of {multiprocess_max_geodes(blueprints[:3])}."
    )
