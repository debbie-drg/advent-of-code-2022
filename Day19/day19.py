import sys
from copy import copy
import multiprocessing

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
        self.max_cost_per_resource = [max([robot_cost[index] for robot_cost in self.robot_costs]) for index in range(len(self.robot_costs))]
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

    def enough_materials(self, materials: list[int], number_robots: list[int]) -> list[int]:
        enough = []
        for index in range(len(self.robot_costs) -1, -1, -1): # Reverse to give later robots priority
            if (index == 3 or number_robots[index] < self.max_cost_per_resource[index]) and all(
                [
                    material >= cost
                    for material, cost in zip(materials, self.robot_costs[index])
                ]
            ):
                enough.append(index)
        # We stop building robots when we have enough to cover demand in one minute.
        # If obsidian or geode can be built, we build it.
        if 2 in enough or 3 in enough:
            enough = [robot for robot in enough if robot in [2,3]]
        return enough

    def next_step(
        self, time_remaining: int, materials: list[int], number_robots: list[int]
    ) -> int:
        to_purchase_this_round = self.enough_materials(materials, number_robots)
        materials = self.update_materials(materials, number_robots)
        if time_remaining == 1:
            return materials[3]
        max_geodes = self.next_step(time_remaining - 1, materials, number_robots) # If no purchase
        for robot_type in to_purchase_this_round: # For the possible purchases. Later robots are purchased first.
            max_geodes = max(
                max_geodes,
                self.next_step(
                    time_remaining - 1,
                    *self.purchase_robot(robot_type, number_robots, materials)
                ),
            )
        return max_geodes

    def max_geodes(self, time_limit: int) -> int:
        number_robots = [1, 0, 0, 0]
        materials = [0, 0, 0, 0]
        return self.next_step(time_limit, materials, number_robots)

    def quality_level(self, time_limit: int) -> int:
        return self.max_geodes(time_limit)


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

    def quality_level(blueprint: Blueprint):
        return blueprint.quality_level(24)

    results = 0
    with multiprocessing.Pool() as pool:
        for result in pool.map(quality_level, blueprints):
            results += result
    print(f"The total quality level is {results}.")
