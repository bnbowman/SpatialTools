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
        required=False,
        default=None,
        help="Reference file for RTS sequence lookup",
    )
    return parser
