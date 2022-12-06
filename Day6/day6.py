import sys


def detect_first_marker(datastream: str, lenth_of_indicator: int = 4) -> int:
    for index in range(len(datastream) - lenth_of_indicator):
        current_values = set(datastream[index : index + lenth_of_indicator])
        if len(current_values) == lenth_of_indicator:
            return index + lenth_of_indicator
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
