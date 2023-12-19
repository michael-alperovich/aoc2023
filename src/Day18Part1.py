import pathlib
import re
from enum import StrEnum

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


class Directions(StrEnum):
    UP = 'U'
    RIGHT = 'R'
    DOWN = 'D'
    LEFT = 'L'


MOVE_MATRIX = {
    Directions.UP: (-1, 0),
    Directions.RIGHT: (0, 1),
    Directions.DOWN: (1, 0),
    Directions.LEFT: (0, -1)
}


def main():
    lines = IN_FILE.read_text().split('\n')
    moves = [re.match(r'(.) ([0-9]+) \((#[0-9a-f]+)\)', line).groups() for line in lines]

    coords = []
    m, n = 1, 1
    i, j = 0, 0
    perimeter = 0
    for direction, distance, color in moves:
        distance = int(distance)
        direction = Directions(direction)
        i += MOVE_MATRIX[direction][0] * distance
        j += MOVE_MATRIX[direction][1] * distance
        perimeter += distance
        coords.append((i, j, color))
        m = max(m, i + 1)
        n = max(n, j + 1)

    area = 0
    for ind in range(len(coords)):
        prev, curr = coords[(ind - 1) % len(coords)], coords[ind]
        area += (prev[1] + curr[1]) * (prev[0] - curr[0])
    area = abs(area) // 2 + perimeter // 2 + 1
    OUT_FILE.write_text(str(area))


if __name__ == '__main__':
    main()
