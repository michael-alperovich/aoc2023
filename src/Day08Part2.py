import itertools
import math
import pathlib
import re
from typing import Dict, Tuple

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'
MAP_KEY = {'L': 0, 'R': 1}
START = 'A'
FINISH = 'Z'


class GraphPath:

    def __init__(self, graph, start: str) -> None:
        self.graph = graph
        self.current = start
        self.cnt = 1
        self.history = set(self.current, )
        self.stop = False

    def advance(self, direction: str) -> None:
        nxt = self.graph[self.current][MAP_KEY[direction]]
        if nxt.endswith('Z'):
            self.stop = True
        else:
            self.current = nxt
            self.cnt += 1
            self.history.add(nxt)


def main():
    lines = IN_FILE.read_text().split('\n')
    instructions: Tuple[str] = tuple(lines[0].strip())
    graph: Dict[str, Tuple[str, str]] = {}
    paths = list()
    for line in lines[2:]:
        vertex, left, right = re.match(r'^([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)$', line).groups()
        graph[vertex] = (left, right)
        if vertex.endswith(START):
            paths.append(GraphPath(graph=graph, start=vertex))

    for i in itertools.cycle(instructions):
        flag = False
        for path in paths:
            if not path.stop:
                flag = True
                path.advance(i)
        if not flag:
            break

    ans = paths[0].cnt
    for path in paths:
        ans = ans * path.cnt // math.gcd(ans, path.cnt)
    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
