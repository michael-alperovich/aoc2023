import pathlib
from collections import deque
from typing import List, Tuple

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'
start = (-1, -1)


def parse(i: int, j: int, lines: List[str]) -> List[Tuple[int, int]]:
    global start
    key = {
        '|': [(i - 1, j), (i + 1, j)],
        '-': [(i, j - 1), (i, j + 1)],
        'L': [(i - 1, j), (i, j + 1)],
        'J': [(i - 1, j), (i, j - 1)],
        '7': [(i + 1, j), (i, j - 1)],
        'F': [(i + 1, j), (i, j + 1)],
        '.': [],
        'S': [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    }
    if lines[i][j] == 'S':
        start = (i, j)
    return [v for v in key[lines[i][j]] if 0 <= v[0] < len(lines) and 0 <= v[1] < len(lines[0])]


def main():
    lines = IN_FILE.read_text().split('\n')
    graph = {(i, j): parse(i, j, lines) for j in range(len(lines[0])) for i in range(len(lines))}

    q = deque()
    q.append(start)
    distance = dict()
    distance[start] = 0
    while len(q) != 0:
        v = q.popleft()
        for u in graph[v]:
            if v not in graph[u]:
                continue
            if u not in distance:
                distance[u] = distance[v] + 1
                q.append(u)
    ans = max(distance.values())
    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
