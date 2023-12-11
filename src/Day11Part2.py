import pathlib

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


def calculate_shift(curr: int, prev: int) -> int:
    const = 10 ** 6
    n_skipped = max(curr - prev - 1, 0)
    shift = n_skipped * (const - 1)
    return shift


def main():
    lines = IN_FILE.read_text().split('\n')
    m, n = len(lines), len(lines[0])
    galaxies = []
    for i in range(m):
        for j in range(n):
            if lines[i][j] == '#':
                galaxies.append([i, j])

    row_sorted = sorted(list(range(len(galaxies))), key=lambda x: galaxies[x][0])
    prev_row = 0
    shift = 0
    for i in row_sorted:
        shift += calculate_shift(galaxies[i][0], prev_row)
        prev_row = galaxies[i][0]
        galaxies[i][0] += shift
    col_sorted = sorted(list(range(len(galaxies))), key=lambda x: galaxies[x][1])
    prev_col = 0
    shift = 0
    for j in col_sorted:
        shift += calculate_shift(galaxies[j][1], prev_col)
        prev_col = galaxies[j][1]
        galaxies[j][1] += shift

    ans = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            ans += abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])
    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
