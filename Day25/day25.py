import sys

SNAFU_KEY = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}

SNAFU_INVERSE_KEY = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}


def snafu_to_decimal(snafu_number: str) -> int:
    digits = [SNAFU_KEY[place] for place in snafu_number]
    digits.reverse()
    number = 0
    for index, digit in enumerate(digits):
        number += (5**index) * digit
    return number


def decimal_to_base5(decimal_number: int) -> int:
    number = ""
    division = decimal_number
    while division != 0:
        division, remainder = divmod(division, 5)
        number = str(remainder) + number
    return int(number)


def base5_to_snafu(base5_number: int) -> str:
    number_list = [int(x) for x in str(base5_number)]
    number_list.reverse()
    number_list.append(0)
    snafu_number = ""
    for index in range(len(number_list)):
        if number_list[index] > 2:
            number_list[index] -= 5
            number_list[index + 1] += 1
        snafu_number = SNAFU_INVERSE_KEY[number_list[index]] + snafu_number
    snafu_number = snafu_number.removeprefix("0")
    return snafu_number


def decimal_to_snafu(decimal_number: int) -> str:
    return base5_to_snafu(decimal_to_base5(decimal_number))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"

    fuel_requirement = 0
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            fuel_requirement += snafu_to_decimal(line)

    print(
        f"The total fuel requirement is {fuel_requirement}. In SNAFU, that's {decimal_to_snafu(fuel_requirement)}."
    )
