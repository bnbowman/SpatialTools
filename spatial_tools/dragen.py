
import sys

from collections import defaultdict

def parse(fn, rts_lookup=None):
    data = defaultdict(int)
    with open(fn) as handle:
        handle.readline()
        for line in handle:
            parts = line.strip().split(',')
            assert len(parts) == 2
            rts, count = parts
            data[rts] = int(count)

    if  rts_lookup is None:
        return data

    new_data = defaultdict(int)
    missed = 0
    for rts_seq, value in data.items():
        try:
            rts_id = rts_lookup[rts_seq]
            new_data[rts_id] = value
        except:
            missed += 1

    if missed > 0:
        print("WARNING: Found {} RTS sequences with missing IDs".format(missed))

    return new_data
