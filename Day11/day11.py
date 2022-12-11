import sys


class Monkey:
    def __init__(self, commands: str, divide_worry: bool = True):
        split_commands = split_lines(commands.split("\n"))
        self.test_modulo = int(split_commands[3][-1])
        self.holding_items = [
            int(item_worry_score.removesuffix(","))
            for item_worry_score in split_commands[1][2:]
        ]
        self.global_modulo = 0
        self.divide_worry = divide_worry
        self.items_inspected = 0
        self.worry_operation_marker = split_commands[2][-2]
        self.self_referencing_operation = False
        try:
            self.worry_operation_value = int(split_commands[2][-1])
        except ValueError:
            self.worry_operation_value = 0
        self.monkey_if_true = int(split_commands[4][-1])
        self.monkey_if_false = int(split_commands[5][-1])

    def worry_level_update(self):
        if self.worry_operation_value == 0:
            self.holding_items = [
                (item * item) % self.global_modulo for item in self.holding_items
            ]
        else:
            match self.worry_operation_marker:
                case "*":
                    self.holding_items = [
                        (item * self.worry_operation_value) % self.global_modulo
                        for item in self.holding_items
                    ]
                case "+":
                    self.holding_items = [
                        (item + self.worry_operation_value) % self.global_modulo
                        for item in self.holding_items
                    ]
                case _:
                    raise AssertionError("Wrong operation marker")
        if self.divide_worry:
            self.holding_items = [item // 3 for item in self.holding_items]
        self.items_inspected += len(self.holding_items)

    def worry_test(self) -> list[bool]:
        return [worry_level % self.test_modulo == 0 for worry_level in self.holding_items]

    def monkey_to_throw(self, test_value: bool) -> int:
        return self.monkey_if_true if test_value else self.monkey_if_false

    def throw_at_monkeys(self) -> list[int]:
        return [self.monkey_to_throw(test) for test in self.worry_test()]

    def monkey_keep_away_round(self) -> list[int]:
        self.worry_level_update()
        return self.throw_at_monkeys()

    def monkey_end_round(self):
        self.holding_items = []


class KeepAway:
    def __init__(self, monkeys: list[str], divide_worry: bool = True):
        self.monkeys = []
        global_modulo = 1
        for monkey in monkeys:
            self.monkeys.append(Monkey(monkey, divide_worry))
            global_modulo *= self.monkeys[-1].test_modulo
        for monkey in self.monkeys:
            monkey.global_modulo = global_modulo

    def keep_away_round(self):
        for monkey in self.monkeys:
            monkeys_to_throw = monkey.monkey_keep_away_round()
            for item, destination_monkey in zip(monkey.holding_items, monkeys_to_throw):
                self.monkeys[destination_monkey].holding_items.append(item)
            monkey.monkey_end_round()

    def play_multiple_rounds(self, number_rounds: int):
        for _ in range(number_rounds):
            self.keep_away_round()

    def times_inspected_items(self) -> list[int]:
        return [monkey.items_inspected for monkey in self.monkeys]

    def monkey_business(self) -> int:
        times_inspected = self.times_inspected_items()
        times_inspected.sort(reverse=True)
        return times_inspected[0] * times_inspected[1]


def split_lines(lines: list[str]) -> list[list[str]]:
    lines = [line.strip() for line in lines]
    return [line.split(" ") for line in lines]


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    game_input = open(file_name).read().split("\n\n")

    keep_away = KeepAway(game_input)
    keep_away.play_multiple_rounds(20)
    print(f"The monkey business after 20 rounds is {keep_away.monkey_business()}.")

    keep_away_no_division = KeepAway(game_input, False)
    keep_away_no_division.play_multiple_rounds(10000)
    print(
        f"The monkey business after 10000 rounds with no division is {keep_away_no_division.monkey_business()}."
    )
