from typing import TypedDict

from .datetime.base import BaseDatetime
from .gps import GeoLocation

class LaunchInfo(TypedDict):
    launch_time : BaseDatetime
    gps         : GeoLocation
