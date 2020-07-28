
import sys

from spatial_tools import options, dragen, rts, dnd, plot

def main():
    parser = options.get_parser()
    args = options.parse_args(parser)
    run(dragen_file=args.dragen_output, dnd1_file=args.dnd1_output, dnd2_file=args.dnd2_output, rts_file=args.rts_file)

def run(dragen_file=None, dnd1_file=None, dnd2_file=None, rts_file=None):
    rts_lookup = None
    if rts_file is not None:
        rts_lookup = rts.parse(rts_file)
    if dragen_file is not None:
        dragen_data = dragen.parse(dragen_file, rts_lookup)
    if dnd2_file is not None:
        dnd2_data = dnd.parse_dnd2(dnd2_file)

    plot.plot(dragen_data, dnd2_data)

if __name__ == "__main__":
    main()
