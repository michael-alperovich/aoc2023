import pathlib
from enum import Enum, auto
from typing import Tuple, List

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


class Directions(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


ORDER = (Directions.NORTH, Directions.WEST, Directions.SOUTH, Directions.EAST)
N_CYCLES = 1000000000


def tilt(platform: List[List[str]], rocks: List[Tuple[int, int]], direction: Directions):
    if direction == Directions.NORTH:
        offset = (-1, 0)
        sorted_rocks = sorted(rocks, key=lambda x: x[0])
    elif direction == Directions.EAST:
        offset = (0, 1)
        sorted_rocks = sorted(rocks, key=lambda x: -x[1])
    elif direction == Directions.SOUTH:
        offset = (1, 0)
        sorted_rocks = sorted(rocks, key=lambda x: -x[0])
    else:
        offset = (0, -1)
        sorted_rocks = sorted(rocks, key=lambda x: x[1])

    new_platform = [[e for e in row] for row in platform]
    new_rocks = list()
    north_load = 0
    for i, j in sorted_rocks:
        new_i, new_j = i, j
        next_i, next_j = i + offset[0], j + offset[1]
        while 0 <= next_i < len(new_platform) and \
                0 <= next_j < len(new_platform[0]) and \
                new_platform[next_i][next_j] == '.':
            new_i, new_j = next_i, next_j
            next_i, next_j = next_i + offset[0], next_j + offset[1]
        new_platform[i][j], new_platform[new_i][new_j] = new_platform[new_i][new_j], new_platform[i][j]
        new_rocks.append((new_i, new_j))
        north_load += len(new_platform) - new_i

    return new_platform, new_rocks, north_load


def main():
    lines = IN_FILE.read_text().split('\n')
    platform = [list(line) for line in lines]
    m, n = len(platform), len(platform[0])
    rocks = sorted(
        filter(
            lambda x: platform[x[0]][x[1]] == 'O',
            ((i, j) for j in range(n) for i in range(m))
        )
    )

    north_load = 0
    platform_history = list()
    load_history = list()
    cycle_start = 0
    for _ in range(N_CYCLES):
        for direction in ORDER:
            platform, rocks, north_load = tilt(platform, rocks, direction)
        t_platform = tuple(tuple(e for e in row) for row in platform)
        if t_platform in platform_history:
            cycle_start = platform_history.index(t_platform)
            break
        else:
            platform_history.append(t_platform)
            load_history.append(north_load)

    cycle_length = len(load_history) - cycle_start
    leftover_steps = (N_CYCLES - cycle_start) % cycle_length
    ans = load_history[cycle_start + leftover_steps - 1]
    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
