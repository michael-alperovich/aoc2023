import pathlib

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


def main():
    lines = IN_FILE.read_text().split('\n')
    platform = [list(line) for line in lines]
    m, n = len(platform), len(platform[0])
    round_rocks = sorted(
        filter(
            lambda x: platform[x[0]][x[1]] == 'O',
            ((i, j) for j in range(n) for i in range(m))
        )
    )

    ans = 0
    for i, j in round_rocks:
        new_i = i
        while new_i > 0 and platform[new_i - 1][j] == '.':
            new_i -= 1
        platform[i][j], platform[new_i][j] = platform[new_i][j], platform[i][j]
        ans += m - new_i

    # for row in platform:
    #     print(*row, sep='')

    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
