import collections
import pathlib
from typing import List, Tuple

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'

CARD_MAP = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


def get_card_rank(card: str) -> int:
    if card in CARD_MAP:
        return CARD_MAP[card]
    else:
        return int(card)


def get_hand_type_rank(hand: str) -> int:
    card_cnt = collections.Counter(hand)
    cnt_cnt = collections.Counter(card_cnt.values())
    if 5 in card_cnt.values():
        return 6
    elif 4 in card_cnt.values():
        return 5
    elif 3 in card_cnt.values() and 2 in card_cnt.values():
        return 4
    elif 3 in card_cnt.values():
        return 3
    elif 2 in card_cnt.values() and cnt_cnt[2] == 2:
        return 2
    elif 2 in card_cnt.values():
        return 1
    else:
        return 0


def sorting_key(hand_info: List) -> Tuple[int, Tuple[int]]:
    hand, _ = hand_info
    type_rank = get_hand_type_rank(hand)
    card_ranks = map(get_card_rank, hand)
    key = type_rank, tuple(card_ranks)
    return key


def main():
    lines = IN_FILE.read_text().split('\n')
    hands = [[line.split()[0], int(line.split()[1])] for line in lines]
    hands.sort(key=sorting_key)
    ans = sum(((i + 1) * h[1] for i, h in enumerate(hands)))
    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
