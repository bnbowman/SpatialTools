
import sys

def parse(fn, rts_lookup=None):
    data = dict()
    with open(fn) as handle:
        handle.readline()
        for line in handle:
            parts = line.strip().split()
            assert len(parts) == 2
            rts, count = parts
            data[rts] = int(count)

    return data
