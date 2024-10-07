"""
ZTF2MMT: Easily submit ZTF sources to the MMT/Binospec queue
"""

__version__ = "0.0.1"
__author__ = 'Nabeel Rehemtulla'
__credits__ = 'Northwestern University, CIERA'

from . import fritz_finderchart
from . import args
from . import ztf2mmt

import os
MMTAPIKEY = os.getenv("MMTAPIKEY")
FRITZAPIKEY = os.getenv("FRITZAPIKEY")
