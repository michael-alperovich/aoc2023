import pathlib
from collections import deque
from enum import StrEnum, auto
from typing import List, Deque

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


class Directions(StrEnum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class Beam:
    def __init__(self, i: int, j: int, direction: Directions) -> None:
        self.i = i
        self.j = j
        self.direction = direction

    def move(self):
        if self.direction == Directions.UP:
            self.i -= 1
        elif self.direction == Directions.RIGHT:
            self.j += 1
        elif self.direction == Directions.DOWN:
            self.i += 1
        elif self.direction == Directions.LEFT:
            self.j -= 1

    def process_tile(self, grid: List[List[str]]) -> List['Beam']:
        self.move()
        if not (0 <= self.i < len(grid) and 0 <= self.j < len(grid[0])):
            return []
        tile = grid[self.i][self.j]
        if tile == '.':
            return [self]
        elif tile == '\\':
            if self.direction == Directions.UP:
                self.direction = Directions.LEFT
            elif self.direction == Directions.RIGHT:
                self.direction = Directions.DOWN
            elif self.direction == Directions.DOWN:
                self.direction = Directions.RIGHT
            elif self.direction == Directions.LEFT:
                self.direction = Directions.UP
            return [self]
        elif tile == '/':
            if self.direction == Directions.UP:
                self.direction = Directions.RIGHT
            elif self.direction == Directions.RIGHT:
                self.direction = Directions.UP
            elif self.direction == Directions.DOWN:
                self.direction = Directions.LEFT
            elif self.direction == Directions.LEFT:
                self.direction = Directions.DOWN
            return [self]
        elif tile == '-':
            if self.direction in (Directions.RIGHT, Directions.LEFT):
                return [self]
            else:
                return [Beam(self.i, self.j, Directions.RIGHT), Beam(self.i, self.j, Directions.LEFT)]
        elif tile == '|':
            if self.direction in (Directions.UP, Directions.DOWN):
                return [self]
            else:
                return [Beam(self.i, self.j, Directions.UP), Beam(self.i, self.j, Directions.DOWN)]
        else:
            raise ValueError(f'Unknown tile type {tile}')


def main():
    lines = IN_FILE.read_text().split('\n')
    grid = [list(line) for line in lines]
    ans = 0
    starting_beams = []
    for i in range(len(grid)):
        starting_beams.append(Beam(i, -1, Directions.RIGHT))
        starting_beams.append(Beam(i, len(grid[0]), Directions.LEFT))
    for j in range(len(grid)):
        starting_beams.append(Beam(-1, j, Directions.DOWN))
        starting_beams.append(Beam(len(grid), j, Directions.UP))

    for start in starting_beams:
        visited = set()
        history = set()
        queue: Deque[Beam] = deque()
        queue.append(start)
        while len(queue) != 0:
            b = queue.popleft()
            for nb in b.process_tile(grid=grid):
                visited.add((nb.i, nb.j))
                if (nb.i, nb.j, nb.direction) not in history:
                    history.add((nb.i, nb.j, nb.direction))
                    queue.append(nb)
        ans = max(ans, len(visited))

    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
