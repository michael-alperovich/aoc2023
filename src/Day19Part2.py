import pathlib
from collections import deque
from typing import Tuple, Deque

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


class PartRange:
    ATTRS = ('x', 'm', 'a', 's')

    def __init__(self, x=None, m=None, a=None, s=None) -> None:
        self.x = x or (1, 4000)
        self.m = m or (1, 4000)
        self.a = a or (1, 4000)
        self.s = s or (1, 4000)

    def __repr__(self) -> str:
        return f'<PartRange {self.x=} {self.m=} {self.a=} {self.s=}>'

    def is_valid(self) -> bool:
        return all((getattr(self, r)[0] <= getattr(self, r)[1] for r in self.ATTRS))

    def invalidate(self) -> None:
        self.x = (0, -1)

    def copy(self) -> 'PartRange':
        return PartRange(self.x, self.m, self.a, self.s)

    def split_by_rule(self, symbol: str, param: str, number: int) -> Tuple['PartRange', 'PartRange']:
        pass_range, fail_range = self.copy(), self.copy()
        if symbol == '<':
            rating_rng = getattr(self, param)
            setattr(pass_range, param, (rating_rng[0], number - 1))
            setattr(fail_range, param, (number, rating_rng[1]))
        elif symbol == '>':
            rating_rng = getattr(self, param)
            setattr(pass_range, param, (number + 1, rating_rng[1]))
            setattr(fail_range, param, (rating_rng[0], number))
        else:
            fail_range.invalidate()
        return pass_range, fail_range

    def calculate_combinations(self) -> int:
        if not self.is_valid():
            return 0
        else:
            return ((self.x[1] - self.x[0] + 1) *
                    (self.m[1] - self.m[0] + 1) *
                    (self.a[1] - self.a[0] + 1) *
                    (self.s[1] - self.s[0] + 1))


class Workflow:
    ACCEPTED = 'A'
    REJECTED = 'R'

    def __init__(self, desc: str) -> None:
        self.name = desc.split('{')[0]
        self.rules = []

        rules_desc = desc.split('{')[1].split('}')[0].split(',')
        for rule in rules_desc:
            if '<' in rule or '>' in rule:
                symbol = '>' if '>' in rule else '<'
                param = rule.split(symbol)[0]
                number = int(rule.split(symbol)[1].split(':')[0])
                destination = rule.split(':')[1]
                self.rules.append((symbol, param, number, destination))
            else:
                self.rules.append((None, None, None, rule))


def main():
    lines = IN_FILE.read_text().split('\n')
    workflows = {}
    for line in lines:
        if line == '':
            break
        else:
            w = Workflow(line)
            workflows[w.name] = w

    ans = 0
    queue: Deque[Tuple[str, PartRange]] = deque()
    queue.append(('in', PartRange()))
    while len(queue) > 0:
        workflow_name, part_range = queue.popleft()
        if workflow_name == Workflow.ACCEPTED:
            ans += part_range.calculate_combinations()
            continue
        elif workflow_name == Workflow.REJECTED:
            continue
        workflow = workflows[workflow_name]
        for symbol, param, number, destination in workflow.rules:
            if not part_range.is_valid():
                break
            else:
                pass_range, fail_range = part_range.split_by_rule(symbol, param, number)
                if pass_range.is_valid():
                    queue.append((destination, pass_range))
                part_range = fail_range

    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
