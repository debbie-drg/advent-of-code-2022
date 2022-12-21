import sys


class MonkeyMath:
    def __init__(self, monkeys: str) -> None:
        monkeys_list = monkeys.splitlines()
        self.monkeys = dict()
        for monkey in monkeys_list:
            monkey = monkey.split(" ")
            name = monkey[0].removesuffix(":")
            self.monkeys[name] = Monkey(monkey)
        for monkey in self.monkeys:
            if self.monkeys[monkey].children is not None:
                child_0 = self.monkeys[monkey].children[0]
                self.monkeys[child_0].parent = monkey
                child_1 = self.monkeys[monkey].children[1]
                self.monkeys[child_1].parent = monkey

    @staticmethod
    def match_operation(value_0: int, value_1: int, operation_marker: str) -> int:
        match operation_marker:
            case "*":
                return value_0 * value_1
            case "/":
                return value_0 // value_1
            case "+":
                return value_0 + value_1
            case "-":
                return value_0 - value_1
            case other:
                raise ValueError
    
    @staticmethod
    def match_opposite_operation(answer: int, other_branch: int, operation_marker: str, human_first: bool) -> int:
        match operation_marker:
            case "+":
                return answer - other_branch
            case "*":
                return answer // other_branch
            case "-":
                if human_first:
                    return answer + other_branch
                return other_branch - answer
            case "/":
                if human_first:
                    return answer * other_branch
                return other_branch // answer
            case other:
                raise ValueError


    def yell(self, monkey: str) -> int:
        if self.monkeys[monkey].value is not None:
            return self.monkeys[monkey].value
        value_child_0 = self.yell(self.monkeys[monkey].children[0])
        value_child_1 = self.yell(self.monkeys[monkey].children[1])
        operation_marker = self.monkeys[monkey].operation
        return self.match_operation(value_child_0, value_child_1, operation_marker)

    def root_human_path(self) -> list[str]:
        current_monkey = "humn"
        path = [current_monkey]
        while self.monkeys[current_monkey].parent != "root":
            current_monkey = self.monkeys[current_monkey].parent
            path.append(current_monkey)
        path.reverse()
        return path

    def yell_human(self) -> int:
        root_human_path = self.root_human_path()
        answer = self.yell([child for child in self.monkeys["root"].children if child != root_human_path[0]][0])
        for element in root_human_path[1:]:
            parent = self.monkeys[element].parent
            operation_marker = self.monkeys[parent].operation
            sibling = [child for child in self.monkeys[parent].children if child != element][0]
            other_value = self.yell(sibling)
            human_first = self.monkeys[parent].children[0] == element
            answer = self.match_opposite_operation(answer, other_value, operation_marker, human_first)
        return answer



class Monkey:
    def __init__(self, monkey_line: list[str]) -> None:
        self.name = monkey_line[0].removesuffix(":")
        if len(monkey_line) == 4:
            self.children = [monkey_line[1], monkey_line[3]]
            self.value = None
            self.operation = monkey_line[2]
        else:
            self.value = int(monkey_line[1])
            self.children = None


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"

    monkey_math = MonkeyMath(open(file_name).read())
    print(f"The root monkey yells {monkey_math.yell('root')}.")
    print(f"To match the root, you have to yell {monkey_math.yell_human()}.")
