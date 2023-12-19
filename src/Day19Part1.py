import pathlib
from typing import List, Tuple, Callable

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


class Part:

    def __init__(self, desc: str) -> None:
        numbers = ''.join(filter(lambda x: x.isdigit() or x == '=', desc)).split('=')[1:]
        self.x, self.m, self.a, self.s = map(int, numbers)

    def rating_sum(self) -> int:
        return self.x + self.m + self.a + self.s


class Workflow:
    ACCEPTED = 'A'
    REJECTED = 'R'

    @staticmethod
    def action_generator(symbol: str, param: str, number: int) -> Callable:
        def action(part: Part) -> bool:
            if symbol == '>':
                return getattr(part, param) > number
            else:
                return getattr(part, param) < number

        return action

    def __init__(self, desc: str) -> None:
        self.name = desc.split('{')[0]
        self.rules: List[Tuple[Callable, str]] = []

        rules_desc = desc.split('{')[1].split('}')[0].split(',')
        for rule in rules_desc:
            if '<' in rule or '>' in rule:
                symbol = '>' if '>' in rule else '<'
                param = rule.split(symbol)[0]
                number = int(rule.split(symbol)[1].split(':')[0])
                destination = rule.split(':')[1]
                self.rules.append((self.action_generator(symbol, param, number), destination))
            else:
                self.rules.append((lambda x: True, rule))

    def process_part(self, part: Part) -> str | bool:
        for cond, destination in self.rules:
            if cond(part):
                if destination == self.ACCEPTED:
                    return True
                elif destination == self.REJECTED:
                    return False
                else:
                    return destination


def main():
    lines = IN_FILE.read_text().split('\n')
    workflows = {}
    parts = []
    matching_workflows = True
    for line in lines:
        if line == '':
            matching_workflows = False
            continue
        if matching_workflows:
            w = Workflow(line)
            workflows[w.name] = w
        else:
            parts.append(Part(line))

    ans = 0
    for part in parts:
        result = 'in'
        while not isinstance(result, bool):
            result = workflows[result].process_part(part)
        if result:
            ans += part.rating_sum()

    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
