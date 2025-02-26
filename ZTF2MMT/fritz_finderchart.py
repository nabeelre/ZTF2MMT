"""
Written 06/26/24
Contact Nabeel Rehemtulla nabeelr@u.northwestern.edu with issues
"""
from datetime import datetime
import requests
import argparse
import os

FRITZAPIKEY = os.getenv("FRITZAPIKEY")
headers = {'Authorization': f'token {FRITZAPIKEY}'}


class SingleOrList(argparse.Action):
    """
    Custom class to handle passing a single or a list of values for an argument
    """
    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            setattr(namespace, self.dest, values)
        else:
            setattr(namespace, self.dest, [values])


def get_finder(ZTFID, image_source, use_ztfref, num_offset_stars):
    """
    Get finder chart for a single ZTF source
    """
    endpoint = f"https://fritz.science/api/sources/{ZTFID}/finder"
    params = {
        "facility": "Keck",
        "image_source": image_source,
        "use_ztfref": use_ztfref,
        "num_offset_stars": num_offset_stars
    }
    r = requests.get(endpoint, headers=headers, params=params)

    if r.status_code == 200:
        if not os.path.exists("finders"):
            os.makedirs("finders")
        with open(f"finders/{ZTFID}_finderchart.pdf", "wb") as pdf_file:
            pdf_file.write(r.content)
            print("Successfully downloaded finding chart for", ZTFID)
    else:
        print("Failed to fetch finding chart for", ZTFID)
        print(r.text)


def get_starlist(ZTFID, facility, use_ztfref, num_offset_stars, obstime):
    """
    Get starlist entry for sources formatted for specified facility
    """
    endpoint = f"https://fritz.science/api/sources/{ZTFID}/offsets"
    params = {
        "facility": facility,
        "use_ztfref": use_ztfref,
        "num_offset_stars": num_offset_stars,
        "obstime": obstime
    }
    r = requests.get(endpoint, headers=headers, params=params)

    if r.status_code == 200:
        starlist = r.json().get("data", {}).get("starlist_str", "")
        starlist = starlist.replace("&nbsp;", " ")

    if r.status_code != 200 or starlist == "":
        print("Failed to fetch finding chart for", ZTFID)
        print(r.text)
        return

    return starlist+"\n"


if __name__ == "__main__":
    """
    Usage examples:
    python fritz_finderchart.py --sources ZTF24aaozxhx
    python fritz_finderchart.py --sources ZTF24aaozxhx ZTF24aatbpbr
    python fritz_finderchart.py --sources ZTF24aaozxhx ZTF24aatbpbr \
        --image_source desi --use_gaia_pos --num_offset_stars 4
    """
    parser = argparse.ArgumentParser(
        description="Get finder charts for ZTF sources from Fritz"
    )
    parser.add_argument(
        '--sources', action=SingleOrList, nargs="+", required=True,
        help="Which ZTF sources to generate finding chart for"
    )
    parser.add_argument(
        '--image_source', type=str, required=False, default="ps1",
        help="Source of image used in finding chart: 'desi', 'dss', 'ztfref', or 'ps1'"
    )
    parser.add_argument(
        '--use_gaia_pos', dest='use_gaia_pos', action='store_true', required=False,
        help="If provided use Gaia DR3 for offset star positions, otherwise use ZTF references"
    )
    parser.add_argument(
        '--num_offset_stars', type=int, required=False, default=3,
        help="Number of offset stars to show [0,4]"
    )
    parser.add_argument(
        '--facility', type=str, required=False, default="Keck",
        help="Facility to prepare starlist for"
    )

    args = parser.parse_args()

    assert args.image_source in ['desi', 'dss', 'ztfref', 'ps1']
    assert (args.num_offset_stars >= 0) and (args.num_offset_stars <= 4)
    assert args.facility in ["Keck", "Shane", "P200", "P200-NGPS"]
    use_ztfref = not args.use_gaia_pos
    ZTFIDs = args.sources
    print("Fetching finding charts for", ZTFIDs)
    print(
        f"Using {args.image_source} reference images and",
        f"{'ztfref' if use_ztfref else 'Gaia DR3'} positions",
        f"for {args.num_offset_stars} offset stars",
        f"with a starlist formatted for {args.facility}"
    )

    starlist = ""
    for ZTFID in ZTFIDs:
        get_finder(ZTFID, args.image_source, use_ztfref, args.num_offset_stars)
        starlist += get_starlist(
            ZTFID, args.facility, use_ztfref, args.num_offset_stars,
            datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        )

    with open("finders/starlist.txt", "w") as f:
        f.write(starlist)
    print(starlist)
