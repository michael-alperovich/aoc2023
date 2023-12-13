import pathlib
from typing import List, Optional

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


def find_symmetry(pattern: List[List[str]], axis: int = 0) -> Optional[int]:
    if axis == 0:
        pattern = [*zip(*pattern)]
    for i in range(len(pattern) - 1):
        symmetry = True
        for j in range(min(i + 1, len(pattern) - i - 1)):
            for k in range(len(pattern[0])):
                if pattern[i - j][k] != pattern[i + j + 1][k]:
                    symmetry = False
                    break
            if not symmetry:
                break
        if symmetry:
            if axis == 0:
                return i + 1
            elif axis == 1:
                return (i + 1) * 100


def main():
    lines = IN_FILE.read_text().split('\n')
    pattern = []
    ans = 0
    for line in lines + ['']:
        if line:
            pattern.append(list(line))
        else:
            ans += find_symmetry(pattern, axis=0) or find_symmetry(pattern, axis=1)
            pattern.clear()
    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
