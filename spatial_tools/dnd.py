
from collections import defaultdict

def parse_dnd1(fn):
    pass

def parse_dnd2(fn):
    data = defaultdict(int)
    with open(fn) as handle:
        for line in handle:
            parts = line.strip().split()
            assert len(parts) == 2
            rts, count = parts
            data[rts] = int(count)
    return data
