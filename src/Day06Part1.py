import math
import pathlib
from functools import reduce

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


def solve(total_time: int, max_distance: int) -> int:
    # equation: t * (total_time - t) > max_distance => t * total_time - t ** 2 - max_distance > 0
    a = -1
    b = total_time
    c = -max_distance
    min_time = math.ceil((-b + math.sqrt(b ** 2 - 4 * a * c)) // 2 * a)
    max_time = math.floor((-b - math.sqrt(b ** 2 - 4 * a * c)) // 2 * a)
    ans = max_time - min_time + 1
    if min_time * (total_time - min_time) <= max_distance:
        ans -= 1
    if max_time * (total_time - max_time) <= max_distance:
        ans -= 1
    return max(ans, 0)


def main():
    lines = IN_FILE.read_text().split('\n')
    times = map(int, filter(lambda x: x != '', lines[0].split()[1:]))
    distances = map(int, filter(lambda x: x != '', lines[1].split()[1:]))
    answer = reduce(
        lambda x, y: x * y,
        map(
            lambda x: solve(*x),
            zip(times, distances)
        )
    )
    OUT_FILE.write_text(str(answer))


if __name__ == '__main__':
    main()
