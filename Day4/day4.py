from itertools import tee


def intervals_contained(intervals: list[list[int]]) -> bool:
    return (intervals[0][0] - intervals[1][0]) * (
        intervals[0][1] - intervals[1][1]
    ) <= 0


def intervals_overlap(intervals: list[list[int]]) -> bool:
    return max(intervals[0][0], intervals[1][0]) <= min(
        intervals[0][1], intervals[1][1]
    )


def split_sections_into_intervals(string: str) -> list[list[int]]:
    return [
        [int(number) for number in item.split("-")] for item in string.split(sep=",")
    ]


with open("input.txt") as f:
    data = f.read().split(sep="\n")
    data.remove("")
    interval_extremes_1, interval_extremes_2 = tee(
        map(split_sections_into_intervals, data), 2
    )
    score_round_1 = sum(map(intervals_contained, interval_extremes_1))
    score_round_2 = sum(map(intervals_overlap, interval_extremes_2))

print(f"The number of overlaps in round one is {score_round_1}")
print(f"The number of overlaps in round two is {score_round_2}")
