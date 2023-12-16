import functools
import pathlib

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


@functools.cache
def custom_hash(s: str) -> int:
    h = 0
    for c in s:
        h = (h + ord(c)) * 17 % 256
    return h


def main():
    steps = IN_FILE.read_text().replace('\n', '').split(',')
    boxes = [[] for _ in range(256)]
    power_map = [{} for _ in range(256)]
    for step in steps:
        if '-' in step:
            label = step.split('-')[0]
            box_number = custom_hash(label)
            if label in power_map[box_number]:
                del power_map[box_number][label]
                boxes[box_number].remove(label)
        else:
            label = step.split('=')[0]
            box_number = custom_hash(label)
            lens_power = int(step.split('=')[1])
            if label in power_map[box_number]:
                power_map[box_number][label] = lens_power
            else:
                boxes[box_number].append(label)
                power_map[box_number][label] = lens_power

    ans = 0
    for i, box in enumerate(boxes):
        for j, label in enumerate(boxes[i]):
            ans += (i + 1) * (j + 1) * power_map[i][label]

    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
