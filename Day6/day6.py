import sys

VALUE_A = ord("a")


def detect_first_marker_old(datastream: str, lenth_of_indicator: int = 4) -> int:
    for index in range(len(datastream) - lenth_of_indicator):
        current_values = set(datastream[index : index + lenth_of_indicator])
        if len(current_values) == lenth_of_indicator:
            return index + lenth_of_indicator
    return 0


def detect_first_marker(datastream: str, lenth_of_indicator: int = 4) -> int:
    # We take a sliding window perspective
    counts = [0] * 26
    unique = 0

    # We populate for the first letters, up to the length of the indicator:
    for char in datastream[:lenth_of_indicator]:
        current_ord = ord(char) - VALUE_A
        counts[current_ord] += 1
        if counts[current_ord] == 1:
            unique += 1

    for index in range(len(datastream) - lenth_of_indicator - 1):
        leaving_ord = ord(datastream[index]) - VALUE_A
        counts[leaving_ord] -= 1
        if counts[leaving_ord] == 0:
            unique -= 1
        entering_ord = ord(datastream[index + lenth_of_indicator]) - VALUE_A
        counts[entering_ord] += 1
        if counts[entering_ord] == 1:
            unique += 1
        if unique == lenth_of_indicator:
            return index + lenth_of_indicator + 1
    return 0


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    text = open(file_name).read().split(sep="\n")
    text.remove("")
    start_of_packet = list(map(detect_first_marker, text))
    start_of_message = list(map(lambda x: detect_first_marker(x, 14), text))

    print(
        f"The first start-of-packet marker for the given message/s at {start_of_packet}"
    )
    print(
        f"The first start-of-message marker for the given message/s at {start_of_message}"
    )
