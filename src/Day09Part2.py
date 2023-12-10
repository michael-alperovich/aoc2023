import pathlib
from typing import List

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


def solve(sequence: List[int]) -> int:
    diffs = [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]
    if all((n == 0 for n in diffs)):
        return sequence[0]
    else:
        return sequence[0] - solve(diffs)


def main():
    lines = IN_FILE.read_text().split('\n')
    sequences = [[int(n) for n in line.split()] for line in lines]
    answer = sum(map(solve, sequences))
    OUT_FILE.write_text(str(answer))


if __name__ == '__main__':
    main()
