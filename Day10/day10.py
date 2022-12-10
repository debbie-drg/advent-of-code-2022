import sys

FILLED_CHARACTER = "██"
EMPTY_CHARACTER = "░░"

def preprocess_instructions(instructions: str) -> list[list[str]]:
    split_instructions = instructions.split("\n")
    split_instructions.remove("")
    split_instructions = [instruction.split(" ") for instruction in split_instructions]

    return split_instructions


def move_sprite(registry: int) -> list[int]:
    return [registry - 1, registry, registry + 1]


def pixel(is_on: bool) -> str:
    return FILLED_CHARACTER if is_on else EMPTY_CHARACTER


def check_new_line(cycle_count: int) -> str:
    return "\n" if cycle_count % 40 == 0 else ""


def render_display(instructions: list[list[str]]) -> str:
    display = ""
    registry_x = 1
    strength_sum = 0
    cycle_count = 0
    sprite_positions = [0, 1, 2]

    for instruction in instructions:
        display += check_new_line(cycle_count)
        display += pixel(cycle_count % 40 in sprite_positions)
        cycle_count += 1
        if cycle_count % 40 == 20:
            strength_sum += cycle_count * registry_x
        if len(instruction) == 2:
            display += check_new_line(cycle_count)
            display += pixel(cycle_count % 40 in sprite_positions)
            cycle_count += 1
            if cycle_count % 40 == 20:
                strength_sum += cycle_count * registry_x
            registry_x += int(instruction[1])
            sprite_positions = move_sprite(registry_x)
    return strength_sum, display


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"

    parsed_instructions = preprocess_instructions(open(file_name).read())

    strenth_sum, display = render_display(parsed_instructions)
    print(f"The sum of signal strengths is {strenth_sum}.")

    print(f"\nHere's what the display looks like.")
    print(display)
