import pathlib
from typing import List

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


class Range:

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end
        self._removed: List['Range'] = []

    def intersects(self, other: 'Range') -> bool:
        return (self.start <= other.start <= self.end) or (other.start <= self.start <= other.end)

    def intersection(self, other: 'Range') -> 'Range':
        intersection_start = max(self.start, other.start)
        intersection_end = min(self.end, other.end)
        return Range(intersection_start, intersection_end)

    def remove(self, other: 'Range') -> None:
        if self.intersects(other):
            self._removed.append(other)

    def calculate_leftovers(self):
        self._removed.append(Range(10 ** 10, 10 ** 10))
        self._removed.sort(key=lambda r: r.start)
        ranges = []
        removed_end = self.start - 1
        for other in self._removed:
            if other.end <= removed_end:
                continue
            else:
                leftover_start = removed_end + 1
                removed_end = other.end
                if leftover_start < other.start - 1:
                    ranges.append(Range(leftover_start, min(other.start - 1, self.end)))
                if self.end <= removed_end:
                    break
        return ranges

    def __repr__(self):
        return f'<Range [{self.start}, {self.end}]>'


class MapRange:

    def __init__(self, dest_start: int, source_start: int, length: int) -> None:
        self.length = length
        self.source_range = Range(source_start, source_start + length - 1)
        self.dest_range = Range(dest_start, dest_start + length - 1)

    def _map_n_to_dest(self, n: int) -> int:
        return n - self.source_range.start + self.dest_range.start

    def transform_range(self, rng: Range):
        intersection = rng.intersection(self.source_range)
        mapped = Range(self._map_n_to_dest(intersection.start), self._map_n_to_dest(intersection.end))
        rng.remove(intersection)
        return mapped

    def __repr__(self):
        return f'<MapRange {self.source_range} -> {self.dest_range}>'


def main():
    lines = IN_FILE.read_text().split('\n')

    seed_info = lines[0][len('Seeds: '):].split()
    seed_ranges = [
        Range(int(s), int(s) + int(l) - 1)
        for s, l in [seed_info[i:i + 2] for i in range(0, len(seed_info), 2)]
    ]

    maps: List[List[MapRange]] = []
    skip = False
    for line in lines[1:]:
        if skip:
            skip = False
            continue
        elif not line:
            maps.append([])
            skip = True
        else:
            maps[-1].append(MapRange(*map(int, line.strip().split())))

    current_ranges = seed_ranges
    for almanach_map_ranges in maps:
        next_ranges = []
        for r in current_ranges:
            for mr in almanach_map_ranges:
                if r.intersects(mr.source_range):
                    next_ranges.append(mr.transform_range(r))
            next_ranges.extend(r.calculate_leftovers())
        current_ranges = next_ranges

    lowest_location = sorted(current_ranges, key=lambda s: s.start)[0].start
    OUT_FILE.write_text(str(lowest_location))


if __name__ == '__main__':
    main()
