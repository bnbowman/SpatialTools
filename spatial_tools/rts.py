
def parse(fn):
    data = dict()
    with open(fn) as handle:
        for line in handle:
            parts = line.strip().split()
            assert len(parts) == 2
            rts_id, rts_seq = parts
            data[rts_seq] = rts_id
    return data
