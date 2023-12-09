import itertools
import pathlib
import re
from typing import Dict, Tuple

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'
MAP_KEY = {'L': 0, 'R': 1}
START_VERTEX = 'AAA'
FINISH_VERTEX = 'ZZZ'


def main():
    lines = IN_FILE.read_text().split('\n')
    instructions: Tuple[str] = tuple(lines[0].strip())
    graph: Dict[str, Tuple[str, str]] = {}
    for line in lines[2:]:
        vertex, left, right = re.match(r'^([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)$', line).groups()
        graph[vertex] = (left, right)

    vertex = START_VERTEX
    cnt = 0
    for i in itertools.cycle(instructions):
        if vertex == FINISH_VERTEX:
            break
        vertex = graph[vertex][MAP_KEY[i]]
        cnt += 1
    OUT_FILE.write_text(str(cnt))


if __name__ == '__main__':
    main()
