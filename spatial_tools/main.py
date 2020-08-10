
import sys

from spatial_tools import options, dragen, rts, dnd, jbruand
from spatial_tools.rts import RtsTable
from spatial_tools.analysis import RtsAnalyzer

def main():
    parser = options.get_parser()
    args = options.parse_args(parser)
    run(args.output_dir, args.rts_file, args.control_prefix, args.limit_of_quantitation, dragen_file=args.dragen_output, jbruand_file=args.jbruand_output, dnd1_file=args.dnd1_output, dnd2_file=args.dnd2_output)

def run(output, rts_file, rts_prefix, quant_limit, dragen_file=None, jbruand_file=None, dnd1_file=None, dnd2_file=None):
    rts_table = RtsTable.from_file(rts_file, rts_prefix)
    analyzer = RtsAnalyzer(output, rts_table, quant_limit)

    print(dragen_file)
    if dragen_file is not None:
        dragen_data = dragen.parse(dragen_file)
        dragen_trans = rts_table.translate(dragen_data)
    if jbruand_file is not None:
        jbruand_data = jbruand.parse(jbruand_file)
        jbruand_trans = rts_table.translate(jbruand_data)
        analyzer.run(dragen_trans, jbruand_trans)
    if dnd1_file is not None:
        dnd1_data = dnd.parse_dnd1(dnd1_file)
        analyzer.run(dragen_trans, dnd1_data)
    if dnd2_file is not None:
        dnd2_data = dnd.parse_dnd2(dnd2_file)
        analyzer.run(dragen_trans, dnd2_data)


if __name__ == "__main__":
    main()
