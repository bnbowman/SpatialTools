
SUMMARY_START = "<Code_Summary>"
SUMMARY_END = "</Code_Summary>"

def parse_dnd1(fn):
    data = dict()
    in_summary = False
    with open(fn) as handle:
        for line in handle:
            line = line.strip()
            if line == SUMMARY_START:
                in_summary = True
                continue
            if line == SUMMARY_END:
                in_summary = False
                continue
            if in_summary:
                parts = line.strip().split(',')
                assert len(parts) == 2
                rts, count = parts
                data[rts] = int(count)
    return data

def parse_dnd2(fn):
    data = dict()
    with open(fn) as handle:
        for line in handle:
            parts = line.strip().split()
            assert len(parts) == 2
            rts, count = parts
            data[rts] = int(count)
    return data
