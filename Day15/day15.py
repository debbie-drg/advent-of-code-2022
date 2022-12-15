import sys


def manhattan_distance(location_1, location_2):
    return abs(location_1[0] - location_2[0]) + abs(location_1[1] - location_2[1])


def line_intersection(line_1, line_2):
    x = (line_2[1] - line_1[1]) / (line_1[0] - line_2[0])
    y = line_1[0] * x + line_1[1]
    return (x, y)


def parse_input(input_string):
    positions = []
    split_string = input_string.split("\n")
    split_string.remove("")
    for line in split_string:
        line = line.split(" ")
        positions.append(
            list(map(int, [line[2][2:-1], line[3][2:-1], line[8][2:-1], line[9][2:]]))
        )
    return positions


class Interval:
    def __init__(self, extremes: list[int]):
        self.extremes = extremes

    def __repr__(self) -> str:
        return f"[{self.extremes[0]}, {self.extremes[1]}]"

    def __len__(self):
        if self.extremes == []:
            return 0
        return self.extremes[1] - self.extremes[0] + 1

    def contains(self, element: int):
        return self.extremes[0] <= element and element <= self.extremes[1]

    def intersects(self, __o):
        return self.contains(__o.extremes[0]) or self.contains(__o.extremes[1])

    def union(self, __o):
        self.extremes[0] = min(self.extremes[0], __o.extremes[0])
        self.extremes[1] = max(self.extremes[1], __o.extremes[1])


class Intervals:
    def __init__(self, intervals: list[Interval]):
        self.intervals = intervals

    def __repr__(self) -> str:
        return f"Intervals: {self.intervals}"

    def __len__(self):
        self.merge()
        return sum(len(interval) for interval in self.intervals)

    def add(self, interval: Interval):
        if interval.extremes == []:
            return None
        self.intervals.append(interval)
        self.merge()

    def sort(self):
        self.intervals

    def merge(self):
        self.intervals.sort(key=lambda x: x.extremes[0])
        while True:
            changed = False
            for index in range(0, len(self.intervals) - 1):
                if self.intervals[index].intersects(self.intervals[index + 1]):
                    self.intervals[index].union(self.intervals[index + 1])
                    self.intervals.pop(index + 1)
                    changed = True
                    break
            if not changed:
                break


class Sensor:
    def __init__(self, location, beacon_index):
        self.location = location
        self.closest_beacon = beacon_index
        self.beacon_distance = None


class Grid:
    def __init__(self, text_input):
        positions = parse_input(text_input)
        self.beacons = []
        self.sensors = []
        for index, line in enumerate(positions):
            self.sensors.append(Sensor((line[0], line[1]), index))
            self.beacons.append((line[2], line[3]))
            self.sensors[-1].beacon_distance = manhattan_distance(
                self.sensors[-1].location, self.beacons[-1]
            )

    def row_cover_area(self, sensor_index: int, row: int) -> Interval:
        rows_appart = abs(self.sensors[sensor_index].location[1] - row)
        if rows_appart <= self.sensors[sensor_index].beacon_distance:
            start_index = (
                self.sensors[sensor_index].location[0]
                - self.sensors[sensor_index].beacon_distance
                + rows_appart
            )
            end_index = (
                self.sensors[sensor_index].location[0]
                + self.sensors[sensor_index].beacon_distance
                - rows_appart
            )
            return Interval([start_index, end_index])
        return Interval([])

    def number_positions_without_beacon_in_row(self, row: int):
        rows_without_beacon = Intervals([])
        beacons_in_row = set()
        for index in range(len(self.sensors)):
            current_beacon_row = self.row_cover_area(index, row)
            if len(current_beacon_row) != 0:
                if self.beacons[self.sensors[index].closest_beacon][1] == row:
                    beacons_in_row.add(self.beacons[self.sensors[index].closest_beacon])
            rows_without_beacon.add(current_beacon_row)
        return len(rows_without_beacon) - len(beacons_in_row)

    def check_location(self, location: tuple, min_index: int, max_index: int) -> bool:
        return (
            min_index < location[0] < max_index and min_index < location[1] < max_index
        )

    def lines_from_extremes(self, beacon_index):
        location = self.sensors[beacon_index].location
        top = (
            location[0] + self.sensors[beacon_index].beacon_distance + 1,
            location[1],
        )
        bottom = (
            location[0] - self.sensors[beacon_index].beacon_distance - 1,
            location[1],
        )
        lines_pos = [(1, top[1] - top[0]), (1, bottom[1] - bottom[0])]
        lines_neg = [(-1, top[1] + top[0]), (-1, bottom[1] + bottom[0])]
        return lines_pos, lines_neg

    def lines_intersection(self, beacon_1, beacon_2):
        points = []
        lines_pos_1, lines_neg_1 = self.lines_from_extremes(beacon_1)
        lines_pos_2, lines_neg_2 = self.lines_from_extremes(beacon_2)
        for line_1 in lines_pos_1:
            for line_2 in lines_neg_2:
                current_point = line_intersection(line_1, line_2)
                if (current_point[0]==int(current_point[0]) and current_point[1] == int(current_point[1])):
                    points.append((int(current_point[0]), int(current_point[1])))
        for line_1 in lines_neg_1:
            for line_2 in lines_pos_2:
                current_point = line_intersection(line_1, line_2)
                if (current_point[0]==int(current_point[0]) and current_point[1] == int(current_point[1])):
                    points.append((int(current_point[0]), int(current_point[1])))
        return points

    def candidate_distress_beacon(self, min_range: int, max_range: int) -> set:
        candidates = set()
        for index_1 in range(len(self.sensors) - 1):
            for index_2 in range(1, len(self.sensors)):
                new_candidates = self.lines_intersection(index_1, index_2)
                new_candidates = [
                    candidate
                    for candidate in new_candidates
                    if self.check_location(candidate, min_range, max_range)
                ]
                candidates = candidates.union(set(new_candidates))
        return candidates

    def check_if_beacon(self, candidate):
        for sensor_index in range(len(self.sensors)):
            if (
                manhattan_distance(candidate, self.sensors[sensor_index].location)
                <= self.sensors[sensor_index].beacon_distance
            ):
                return False
        else:
            return True

    def find_beacon(self, min_range: int, max_range: int) -> int | None:
        candidates = self.candidate_distress_beacon(min_range, max_range)
        for candidate in candidates:
            if self.check_if_beacon(candidate):
                return candidate[0] * 4000000 + candidate[1]


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    sensors_and_beacons = open(file_name).read()
    sensors_grid = Grid(sensors_and_beacons)
    if file_name == "example.txt":
        print(
            f"In row 10, there are {sensors_grid.number_positions_without_beacon_in_row(10)} positions where the distress beacon can't be."
        )
        print(
            f"The distress beacon frequency is {sensors_grid.find_beacon(min_range = 0, max_range=20)}."
        )
    if file_name == "input.txt":
        print(
            f"In row 2000000, there are {sensors_grid.number_positions_without_beacon_in_row(2000000)} positions where the distress beacon can't be."
        )
        print(
            f"The distress beacon frequency is {sensors_grid.find_beacon(min_range = 0, max_range = 4000000)}."
        )
