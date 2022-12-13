import sys


def preprocess_lists(read_data: str):
    read_data = read_data.removesuffix("\n")
    read_data = read_data.split("\n\n")
    read_data = [lists.split("\n") for lists in read_data]
    parsed_lists = []

    for pair_of_lists in read_data:
        parsed_lists.append([eval(pair_of_lists[0]), eval(pair_of_lists[1])])

    return parsed_lists


def preprocess_all_lists(read_data: str):
    read_data = read_data.replace("\n\n", "\n")
    read_data = read_data.split("\n")
    read_data.remove("")
    parsed_lists = [eval(line) for line in read_data]

    return parsed_lists


def compare_lists(list_1: list, list_2: list):
    value = compare_sublists(list_1, list_2)
    if value == "continue":
        if len(list_1) == 0:
            return True
        return compare_lists(list_1[1:], list_2[1:])
    return value


def compare_sublists(list_1: list, list_2: list):
    if len(list_1) == 0:
        if len(list_2) > 0:
            return True
        return "continue"
    if len(list_2) == 0:
        return False

    # The case where they both are lists
    if isinstance(list_1[0], int) and isinstance(list_2[0], int):
        if list_1[0] < list_2[0]:
            return True
        if list_1[0] > list_2[0]:
            return False
        return compare_sublists(list_1[1:], list_2[1:])

    # The case where one or both are lists.
    # First we convert the next int to list, if needed.
    if isinstance(list_1[0], list) and isinstance(list_2[0], int):
        list_1_to_compare = list_1[0]
        list_2_to_compare = [list_2[0]]
    elif isinstance(list_2[0], list) and isinstance(list_1[0], int):
        list_1_to_compare = [list_1[0]]
        list_2_to_compare = list_2[0]
    else:
        list_1_to_compare = list_1[0]
        list_2_to_compare = list_2[0]

    # We compare the sublists.
    value = compare_sublists(list_1_to_compare, list_2_to_compare)
    if value == "continue":
        return compare_sublists(list_1[1:], list_2[1:])
    return value


def decoder_key(lists_to_sort):
    lists_to_sort.append([[2]])
    lists_to_sort.append([[6]])
    lists_to_sort[0], lists_to_sort[1] = lists_to_sort[1], lists_to_sort[0]
    for index in range(len(lists_to_sort) - 1):
        if not compare_lists(lists_to_sort[index], lists_to_sort[index + 1]):
            lists_to_sort[index + 1], lists_to_sort[index] = (
                lists_to_sort[index],
                lists_to_sort[index + 1],
            )
            for descending_index in range(index, 0, -1):
                if not compare_lists(
                    lists_to_sort[descending_index - 1], lists_to_sort[descending_index]
                ):
                    (
                        lists_to_sort[descending_index - 1],
                        lists_to_sort[descending_index],
                    ) = (
                        lists_to_sort[descending_index],
                        lists_to_sort[descending_index - 1],
                    )
                else:
                    break

    return (lists_to_sort.index([[2]]) + 1) * (lists_to_sort.index([[6]]) + 1)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    lists_to_compare = open(file_name).read()
    parsed_lists = preprocess_lists(lists_to_compare)
    in_order = 0
    for index, pair_of_lists in enumerate(parsed_lists):
        if compare_lists(pair_of_lists[0], pair_of_lists[1]):
            in_order += index + 1

    lists_to_order = preprocess_all_lists(lists_to_compare)

    print(f"The sum of indices of lists in order is {in_order}.")
    print(f"The decoder key is {decoder_key(lists_to_order)}.")
