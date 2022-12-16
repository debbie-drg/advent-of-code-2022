import sys


def parse_data(pipe_data: list[str]) -> list:
    pipe_data.remove("")
    valves = []
    for valve in pipe_data:
        valve = valve.split(" ")
        valve_name = valve[1]
        flow_rate = int(valve[4].removesuffix(";").removeprefix("rate="))
        neighbours = [neighbour.removesuffix(",") for neighbour in valve[9:]]
        valves.append([valve_name, flow_rate, neighbours])
    return valves


class Valve:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.open = False
        self.neighbours = []

    def per_minute_flow(self):
        if self.open:
            return self.capacity
        return 0

    def value_if_open(self, time_left):
        return self.capacity * time_left


class CaveValves:
    def __init__(self, valve_data: list):
        self.valves = []
        self.number_valves = len(valve_data)
        self.valves_open = [False] * self.number_valves
        self.distances_computed = [False] * self.number_valves
        self.distances = [
            [len(valve_data) + 1] * len(valve_data) for _ in range(len(valve_data))
        ]
        for index in range(self.number_valves):
            self.distances[index][index] = 0
        self.indices_dict = dict()
        for index, valve in enumerate(valve_data):
            self.valves.append(Valve(capacity=valve[1]))
            self.indices_dict[valve[0]] = index
            if valve[1] == 0:
                self.valves_open[index] = True
        for index, valve in enumerate(valve_data):
            for neighbour in valve[2]:
                self.distances[self.indices_dict[valve[0]]][
                    self.indices_dict[neighbour]
                ] = 1
                self.valves[self.indices_dict[valve[0]]].neighbours.append(
                    self.indices_dict[neighbour]
                )

    def compute_distances_from(self, index):
        if self.distances_computed[index]:
            return None
        max_distance = self.number_valves + 1
        unvisited = list(range(self.number_valves))
        current_position = index
        tentative_distance = 0
        while unvisited != []:
            tentative_distance = self.distances[index][current_position] + 1
            for neighbour in [
                neighbour
                for neighbour in self.valves[current_position].neighbours
                if neighbour in unvisited
            ]:
                if tentative_distance < self.distances[index][neighbour]:
                    self.distances[index][neighbour] = tentative_distance
                    self.distances[neighbour][index] = tentative_distance
            unvisited.remove(current_position)
            min_unvisited_distance = max_distance
            for position in unvisited:
                if self.distances[index][position] <= min_unvisited_distance:
                    current_position = position
                    min_unvisited_distance = self.distances[index][position]
        self.distances_computed[index] = True

    def max_achievable_score(
        self, current_score, score_per_minute, time_left, candidates
    ):
        max_possible_score = current_score + score_per_minute * time_left
        remaining_flows = sorted(
            [self.valves[candidate].capacity for candidate in candidates], reverse=True
        )
        remaining_flows = remaining_flows[: ((time_left - 1) // 2)]
        for index, flow in enumerate(remaining_flows):
            max_possible_score += (time_left - 2 * (index + 1)) * flow
        return max_possible_score

    def candidate_potential(self, time_left, current_position, candidate):
        distance = self.distances[current_position][candidate]
        return (time_left - distance - 1) * self.valves[candidate].capacity

    def next_move(
        self,
        time_left,
        current_position,
        current_score,
        current_score_per_minute,
        valves_open,
        path,
    ):
        self.compute_distances_from(current_position)
        candidates = [
            valve for valve in range(self.number_valves) if not self.valves_open[valve]
        ]
        if (
            self.max_achievable_score(
                current_score, current_score_per_minute, time_left, candidates
            )
            < self.best_score
        ):
            return None
        any_candidates = False
        for candidate in candidates:
            candidate_distance = self.distances[current_position][candidate]
            if candidate_distance < time_left + 1:
                any_candidates = True
                current_candidate_score = (
                    current_score + (candidate_distance + 1) * current_score_per_minute
                )
                candidate_score_per_minute = (
                    current_score_per_minute + self.valves[candidate].capacity
                )
                valves_open[candidate] = True
                self.next_move(
                    time_left - candidate_distance - 1,
                    candidate,
                    current_candidate_score,
                    candidate_score_per_minute,
                    valves_open,
                    path + [candidate],
                )
                valves_open[candidate] = False
        if not any_candidates:
            current_score += current_score_per_minute * time_left
            self.best_score = max(self.best_score, current_score)
            self.best_path = path

    def pressure_release(self, time_limit):
        start_position = self.indices_dict["AA"]
        self.best_score = 0
        self.next_move(
            time_limit, start_position, 0, 0, self.valves_open, [start_position]
        )


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    pipe_data = open(file_name).read().split("\n")
    valve_data = parse_data(pipe_data)
    cave_valves = CaveValves(valve_data)
    cave_valves.pressure_release(30)
    print(f"The most pressure you can release is {cave_valves.best_score}.")
