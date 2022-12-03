def find_repeated(strings: list[str]) -> str:
    for item in strings[0]:
        if all([item in strings[i] for i in range(1, len(strings))]):
            return item
    return ""


def split_in_half(string: str) -> list[str]:
    split_point = int(len(string) / 2)
    return [string[:split_point], string[split_point:]]


def group_elements(string_list: list[str], number_per_group: int) -> list[list[str]]:
    return [
        [string_list[i] for i in range(start, start + number_per_group)]
        for start in range(0, len(string_list), number_per_group)
    ]


def char_to_point(character: str) -> int:
    number = ord(character)
    return (number - 38) % 58


with open("input.txt") as f:
    input_data = f.read().split("\n")
    input_data.remove("")
    repeated_1 = map(find_repeated, map(split_in_half, input_data))
    repeated_2 = map(find_repeated, group_elements(input_data, number_per_group=3))
    scores_1 = sum(map(char_to_point, repeated_1))
    scores_2 = sum(map(char_to_point, repeated_2))

print(f"The score for part one is {scores_1}")
print(f"The score for part one is {scores_2}")
