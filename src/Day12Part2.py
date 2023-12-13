import pathlib
from functools import cache
from typing import Tuple

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


@cache
def possible(line: str, groups: Tuple[int], line_pos: int, current_groups: Tuple[int], damaged_cnt: int) -> int:
    groups = list(groups)
    current_groups = list(current_groups)
    while True:
        if line_pos >= len(line):
            if damaged_cnt != 0:
                current_groups.append(damaged_cnt)
            if groups == current_groups:
                return 1
            else:
                return 0

        if groups[:len(current_groups)] != current_groups:
            return 0
        elif len(current_groups) > len(groups):
            return 0
        elif len(current_groups) == len(groups) and damaged_cnt > 0:
            return 0
        elif damaged_cnt > 0 and damaged_cnt > groups[len(current_groups)]:
            return 0

        if line[line_pos] == '#':
            damaged_cnt += 1
        elif line[line_pos] == '.':
            if damaged_cnt != 0:
                current_groups.append(damaged_cnt)
                damaged_cnt = 0
        else:
            break
        line_pos += 1

    damaged_possibilities = possible(line, tuple(groups), line_pos + 1, tuple(current_groups), damaged_cnt + 1)
    if damaged_cnt != 0:
        current_groups.append(damaged_cnt)
    working_possibilities = possible(line, tuple(groups), line_pos + 1, tuple(current_groups), 0)
    return damaged_possibilities + working_possibilities


def main():
    lines = IN_FILE.read_text().split('\n')
    ans = 0
    for line in lines:
        conditions, groups = line.strip().split(' ')
        groups = tuple([int(t) for t in groups.split(',')])
        conditions = ((conditions + '?') * 5)[:-1]
        groups *= 5
        ans += possible(conditions, groups, 0, (), 0)
    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
