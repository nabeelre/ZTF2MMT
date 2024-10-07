from astropy.coordinates import Angle
import astropy.units as u
import requests
import pymmt

import ZTF2MMT


def send_to_MMT():
    pass


def query_fritz(ZTFID):
    """
    Queries Fritz for the coordinates and latest magnitude of a given ZTF source.

    Parameters:
        ZTFID (str): The ID of the ZTF source to query.

    Returns:
        tuple: RA in HMS format, Dec in DMS format, and the latest magnitude
    """
    headers = {'Authorization': f'token {ZTF2MMT.FRITZAPIKEY}'}

    # Query for coordinates of source
    endpoint = f"https://fritz.science/api/sources/{ZTFID}"
    r = requests.get(endpoint, headers=headers)

    if not r.ok:
        print(f"Failed to query fritz for {ZTFID} coordinates")
        print(r.text)
        # raise Exception
    data = r.json()['data']

    # Convert RA and Dec from deg to HMS and DMS
    ra = Angle(data['ra'] * u.deg)
    ra_hms = ra.to_string(unit=u.hourangle, sep=':', precision=2)
    ra_hms_parts = ra_hms.split(':')
    ra_hms_parts[0] = ra_hms_parts[0].zfill(2)
    ra_hms = ':'.join(ra_hms_parts)

    dec = Angle(data['dec'] * u.deg)
    dec_dms = dec.to_string(unit=u.deg, sep=':', precision=2, alwayssign=True)
    dec_dms_parts = dec_dms.split(':')
    dec_dms_parts[0] = dec_dms_parts[0][0] + dec_dms_parts[0][1:].zfill(2)
    dec_dms = ':'.join(dec_dms_parts)

    # Query for latest mag measurement of source
    # Limit to ZTF alert photometry
    endpoint = f"https://fritz.science/api/sources/{ZTFID}/photometry"
    r = requests.get(endpoint, headers=headers)

    if not r.ok:
        print(f"Failed to query fritz for {ZTFID} coordinates")
        print(r.text)
        # raise Exception
    data = r.json()['data']

    mjd_max = 0
    mag = 0
    for phot in data:
        if (phot.get('instrument_name') == 'ZTF') &\
           (phot.get('origin', '') != 'alert_fp') &\
           (phot.get('mjd', 0) > mjd_max):
            mjd_max = phot.get('mjd')
            mag = phot.get('mag')

    return ra_hms, dec_dms, round(mag, 1)


def describe_target(target, include_setup=False):
    details = (
        "\n"
        f"{target.objectid} ({target.magnitude} mag)\n"
        f"{target.ra} {target.dec}\n"
        f"{target.observationtype} request for "
        f"{target.numberexposures * target.exposuretime}s "
        f"({target.numberexposures}x{target.exposuretime}s)\n"
        f"{target.notes}\n"
    )
    print(details)

    if include_setup:
        setup = (
            f"{target.grating} grating at {target.centralwavelength} angstroms\n"
            f"{target.filter} filter, {target.slitwidth} slit\n"
        )
        print(setup)


if __name__ == "__main__":
    args = ZTF2MMT.args.parse()

    ra, dec, mag = query_fritz(args.ztfid)
    print("Finished querying Frtiz for mag and coordinates")

    maskid_map = {
        "Longslit0_75": 113,
        "Longslit1": 111,
        "Longslit1_25": 131,
        "Longslit1_5": 114,
        "Longslit5": 112
    }

    payload = {
        "objectid": args.ztfid,
        "ra": ra, "dec": dec, "pa": 0,
        "exposuretime": args.exptime, "numberexposures": args.numexp,
        "priority": args.prio, "targetofopportunity": int(args.too),
        "magnitude": mag,
        "grating": args.grating, "centralwavelength": args.centwav,
        "observationtype": "longslit", "filter": args.filter,
        "slitwidth": args.slitwidth, "maskid": maskid_map[args.slitwidth],
        "visits": 1, "epoch": 2000.0,
        "pm_ra": 0, "pm_dec": 0,
        "instrumentid": 16,
        "notes": args.notes,
    }

    target = pymmt.Target(
        payload=payload,
        token=ZTF2MMT.MMTAPIKEY,
        verbose=False
    )
    print("Target created and validated")

    # target.post()
    # print("Target posted to MMT queue")

    # ZTF2MMT.fritz_finderchart.get_finder(
    #     ZTFID=ZTFID,
    #     image_source="desi",
    #     use_ztfref=False,
    #     num_offset_stars=3
    # )
    # print("Downloaded finder from Fritz")
    # target.upload_finder(finder_path=f"finders/{ZTFID}_finderchart.pdf")
    # print("Uploaded finder to MMT")

    describe_target(target, include_setup=True)
