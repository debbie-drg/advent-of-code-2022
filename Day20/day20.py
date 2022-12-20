import sys


def parse(encrypted_file: str) -> list[int]:
    instructions = encrypted_file.splitlines()
    instructions = [int(element) for element in instructions]
    return instructions


def mix(encrypted_file: list[int], number_times: int = 1) -> list[int]:
    indices = list(range(len(encrypted_file)))
    number_instructions = len(encrypted_file)

    for _ in range(number_times):
        for index, element in enumerate(encrypted_file):
            if element == 0:
                continue
            location = indices.index(index)
            indices.pop(location)
            new_location = (element + location) % (number_instructions - 1)
            if new_location == 0:
                indices.append(index) # This is not really needed but makes the 
                # behaviour match the examples.
            else:
                indices.insert(new_location, index)        
    return [encrypted_file[index] for index in indices]


def decrypt(encrypted_file: list[int], key: int = 811589153):
    encrypted_file = [key * entry for entry in encrypted_file]
    decrypted_file = mix(encrypted_file, number_times=10)
    return decrypted_file


def groove_coordinates(mixed: list[int]) -> list[int]:
    coordinates = []
    number_elements = len(mixed)
    position_0 = mixed.index(0)
    for element in [1000, 2000, 3000]:
        coordinates.append(mixed[(position_0 + element) % number_elements])
    return coordinates


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    encrypted_file = parse(open(file_name).read())
    mixed = mix(encrypted_file)
    print(f"The sum of the groove coordinates is {sum(groove_coordinates(mixed))}.")
    decrypted = decrypt(encrypted_file)
    print(
        f"The sum of the groove coordinates after decryption is {sum(groove_coordinates(decrypted))}."
    )
