import pathlib
from typing import List

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


def possible(line: str, groups: List[int], line_pos: int, current_groups: List[int], damaged_cnt: int) -> int:
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

    damaged_possibilities = possible(line, groups, line_pos + 1, current_groups.copy(), damaged_cnt + 1)
    if damaged_cnt != 0:
        current_groups.append(damaged_cnt)
    working_possibilities = possible(line, groups, line_pos + 1, current_groups.copy(), 0)
    return damaged_possibilities + working_possibilities


def main():
    lines = IN_FILE.read_text().split('\n')
    ans = 0
    for line in lines:
        conditions, groups = line.strip().split(' ')
        groups = [int(t) for t in groups.split(',')]
        ans += possible(conditions, groups, 0, [], 0)
    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
