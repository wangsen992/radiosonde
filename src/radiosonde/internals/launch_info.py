from typing import TypedDict

from .sonde_datetime.base import BaseDatetime
from .gps import GeoLocation

class LaunchInfo(TypedDict):
    launch_time : BaseDatetime
    launch_gps  : GeoLocation
