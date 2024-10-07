import argparse


def parse():
    parser = argparse.ArgumentParser(
        description="Submit ZTF sources to the MMT/Binospec queue"
    )
    parser.add_argument(
        '--ztfid', type=str, required=True,
        help="Which ZTF source to send to MMT"
    )
    parser.add_argument(
        '--exptime', type=int, required=True,
        help="Second of exposure time per exposure"
    )
    parser.add_argument(
        '--numexp', type=int, required=True,
        help="Number of exposures to execute"
    )
    parser.add_argument(
        '--prio', type=int, required=True,
        help="Priority of the request - 1 highest, 3 lowest"
    )
    parser.add_argument(
        '--too', dest='too', action='store_true', required=False,
        help="If provided send as target-of-opportunity trigger"
    )
    parser.add_argument(
        '--notes', type=str, required=True,
        help="Notes to include in request"
    )

    # Set up arguments
    parser.add_argument(
        '--grating', type=int, required=False, default=270,
        help="Grating to use [270, 600, 1000]"
    )
    parser.add_argument(
        '--centwav', type=int, required=False, default=6500,
        help="Cental wavelength for grating (see MMT documentation for limits)"
    )
    parser.add_argument(
        '--slitwidth', type=str, required=False, default="Longslit1",
        help="Slitwidth to use [Longslit0_75, Longslit1, Longslit1_25, Longslit1_5, Longslit5]"
    )
    parser.add_argument(
        '--filter', type=str, required=False, default="LP3800",
        help="Filter to use [LP3800 or LP3500]"
    )

    return parser.parse_args()
