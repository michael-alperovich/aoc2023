import pathlib

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


def custom_hash(s: str) -> int:
    h = 0
    for c in s:
        h = (h + ord(c)) * 17 % 256
    return h


def main():
    steps = IN_FILE.read_text().replace('\n', '').split(',')
    ans = sum(map(custom_hash, steps))
    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
