import functools
import heapq
import pathlib
from enum import StrEnum, auto
from typing import List

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


class Directions(StrEnum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


MIN_STRAIGHT_LENGTH = 4
MAX_STRAIGHT_LENGTH = 10
POSSIBLE_DIRECTIONS = {
    Directions.UP: (Directions.UP, Directions.RIGHT, Directions.LEFT),
    Directions.RIGHT: (Directions.UP, Directions.RIGHT, Directions.DOWN),
    Directions.DOWN: (Directions.RIGHT, Directions.DOWN, Directions.LEFT),
    Directions.LEFT: (Directions.UP, Directions.DOWN, Directions.LEFT)
}
MOVE_MATRIX = {
    Directions.UP: (-1, 0),
    Directions.RIGHT: (0, 1),
    Directions.DOWN: (1, 0),
    Directions.LEFT: (0, -1)
}


@functools.total_ordering
class Position:

    def __init__(self, graph: List[List[int]], i: int, j: int, direction: Directions, cost: int = 0, smc: int = 1):
        self._graph = graph
        self.i = i
        self.j = j
        self.direction = direction
        self.cost = cost
        self.smc = smc

    def get_next_positions(self) -> List['Position']:
        positions = []
        for next_direction in POSSIBLE_DIRECTIONS[self.direction]:
            move = MOVE_MATRIX[next_direction]
            next_i, next_j = self.i + move[0], self.j + move[1]
            next_smc = self.smc + 1 if self.direction == next_direction else 1
            if not (0 <= next_i < len(self._graph) and 0 <= next_j < len(self._graph[0])):
                continue
            if next_direction != self.direction and self.smc < MIN_STRAIGHT_LENGTH:
                continue
            if next_direction == self.direction and self.smc >= MAX_STRAIGHT_LENGTH:
                continue
            next_cost = self.cost + self._graph[next_i][next_j]
            positions.append(Position(self._graph, next_i, next_j, next_direction, next_cost, next_smc))
        return positions

    def __eq__(self, other):
        return self.cost == other.cost and self.smc == other.smc

    def __lt__(self, other):
        if self.cost == other.cost:
            return self.smc < other.smc
        return self.cost < other.cost


def main():
    lines = IN_FILE.read_text().split('\n')
    graph = [[int(t) for t in line] for line in lines]
    best_cost = {}
    heap = []
    heapq.heappush(heap, Position(graph, 1, 0, Directions.DOWN, cost=graph[1][0]))
    heapq.heappush(heap, Position(graph, 0, 1, Directions.RIGHT, cost=graph[0][1]))
    while len(heap) > 0:
        pos = heapq.heappop(heap)
        if pos.i == len(graph) - 1 and pos.j == len(graph[0]) - 1 and pos.smc >= MIN_STRAIGHT_LENGTH:
            OUT_FILE.write_text(str(pos.cost))
            exit()
        for next_pos in pos.get_next_positions():
            key = (next_pos.i, next_pos.j, next_pos.direction, next_pos.smc)
            if key not in best_cost or next_pos.cost < best_cost[key]:
                best_cost[key] = next_pos.cost
                heapq.heappush(heap, next_pos)
    print(best_cost)


if __name__ == '__main__':
    main()
