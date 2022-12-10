import sys


def preprocess_instructions(instructions):
    instructions = instructions.split("\n")
    instructions.remove("")
    instructions = [instruction.split(" ") for instruction in instructions]
    parsed_instructions = []
    for instruction in instructions:
        new_instruction = (
            [instruction[0], int(instruction[1])]
            if len(instruction) == 2
            else instruction
        )
        parsed_instructions.append(new_instruction)

    return parsed_instructions


def signal_strength_sum(instructions):
    registry_x = 1
    strength_sum = 0
    cycle_count = 0

    for instruction in instructions:
        cycle_count += 1
        if cycle_count % 40 == 20:
            strength_sum += cycle_count * registry_x
        if len(instruction) == 2:
            cycle_count += 1
            if cycle_count % 40 == 20:
                strength_sum += cycle_count * registry_x
            registry_x += instruction[1]
    return strength_sum


def move_sprite(registry):
    return [registry - 1, registry, registry + 1]


def line_and_pixel(cycle_count):
    return [cycle_count // 40, cycle_count % 40]


def pixel(is_on: bool):
    return "#" if is_on else "."


def check_new_line(cycle_count):
    return "\n" if cycle_count % 40 == 0 else ""


def render_display(instructions):
    display = ""
    registry_x = 1
    cycle_count = 0
    sprite_positions = [0, 1, 2]

    for instruction in instructions:
        display += check_new_line(cycle_count)
        display += pixel(cycle_count % 40 in sprite_positions)
        cycle_count += 1
        if len(instruction) == 2:
            display += check_new_line(cycle_count)
            display += pixel(cycle_count % 40 in sprite_positions)
            cycle_count += 1
            registry_x += instruction[1]
            sprite_positions = move_sprite(registry_x)
    return display


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"

    parsed_instructions = preprocess_instructions(open(file_name).read())

    strenth_sum = signal_strength_sum(parsed_instructions)
    print(f"The sum of signal strengths is {strenth_sum}.")

    print(f"\nHere's what the display looks like.")
    print(render_display(parsed_instructions))
