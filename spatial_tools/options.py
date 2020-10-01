import os
import os.path as op
import argparse


def parse_args(parser):
    args = parser.parse_args()
    return args


def get_parser():
    """
    Define and parse command-line options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dragen_output",
        required=False,
        default=None,
        help="File of DRAGEN Spatial Analysis results",
    )
    parser.add_argument(
        "-j",
        "--jbruand_output",
        required=False,
        default=None,
        help="File of Jocelyne's manual Spatial Analysis results",
    )
    parser.add_argument(
        "-1",
        "--dnd1_output",
        required=False,
        default=None,
        help="File of analysis results from DND v1",
    )
    parser.add_argument(
        "-2",
        "--dnd2_output",
        required=False,
        default=None,
        help="File of analysis results from DND v2",
    )
    parser.add_argument(
        "-r",
        "--rts_file",
        required=True,
        default=None,
        help="Reference file for RTS sequence lookup",
    )
    parser.add_argument(
        "-p",
        "--control_prefix",
        required=False,
        default="ERCC_",
        help="Reference file for RTS sequence lookup",
    )
    parser.add_argument(
        "-l",
        "--limit_of_quantitation",
        required=False,
        default=5.0,
        type=float,
        help="Minimum UMI count for RTS barcode detection (Set < 0 to disable)",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        required=False,
        default=os.getcwd(),
        help="Output directory",
    )
    return parser
