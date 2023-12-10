import pathlib
import sys
from typing import List, Tuple, Dict, Set

sys.setrecursionlimit(10 ** 5)
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


def dfs(v: Tuple[int, int], graph: Dict, path: List = None, visited: Set = None) -> List[Tuple[int, int]]:
    path = path or []
    visited = visited or set()
    path.append(v)
    visited.add(v)
    answer = None
    for u in graph[v]:
        if v not in graph[u]:
            continue
        elif u == start and len(path) > 2:
            answer = path.copy()
        elif u not in visited:
            answer = answer or dfs(u, graph, path, visited)
    path.pop()
    return answer


def get_inside_points(lines: List[str], cycle: Set) -> Set:
    points_inside = set()
    up_corners = ['L', 'J']
    horizontal_start_symbol = None
    for i in range(len(lines)):
        n_edges_crossed = 0
        for j in range(len(lines[0])):
            if (i, j) in cycle:
                if lines[i][j] == '|':
                    n_edges_crossed += 1
                elif lines[i][j] == '-':
                    continue
                else:
                    if horizontal_start_symbol is None:
                        horizontal_start_symbol = lines[i][j]
                    else:
                        if (horizontal_start_symbol in up_corners) != (lines[i][j] in up_corners):
                            n_edges_crossed += 1
            else:
                if n_edges_crossed % 2 == 1:
                    points_inside.add((i, j))
    return points_inside


def main():
    lines = IN_FILE.read_text().split('\n')
    graph = {(i, j): parse(i, j, lines) for j in range(len(lines[0])) for i in range(len(lines))}
    cycle = dfs(start, graph)
    points_inside = get_inside_points(lines=lines, cycle=set(cycle))
    OUT_FILE.write_text(str(len(points_inside)))
    # print(points_inside)
    # for i in range(len(lines)):
    #     for j in range(len(lines[0])):
    #         if (i, j) in cycle:
    #             print(lines[i][j], end='')
    #         elif (i, j) in points_inside:
    #             print('I', end='')
    #         else:
    #             print('O', end='')
    #     print()


if __name__ == '__main__':
    main()
