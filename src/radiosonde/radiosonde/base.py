from abc import ABC, abstractmethod

from ..internals.launch_info import LaunchInfo as LaunchInfo
from ..internals.gps import GeoLocation
from ..internals.sonde_datetime.base import BaseDatetime as SondeDatetime

class BaseRadiosondeComponent(ABC):
    """Define an interface for working with radiosonde data"""

    def __validate(self) -> bool:
        """Validate (extension required)"""
        pass

    @abstractmethod
    def is_list(self) -> bool:
        pass

    @abstractmethod
    def some_operation(self)  -> str:
        """Defines the interface here"""
        pass

    # Variable accessors
    @property
    @abstractmethod
    def height(self):
        """return the height values of (collection of) sondes"""
        pass

    @property
    @abstractmethod
    def pressure(self):
        """return the pressure values of (collection of) sondes"""
        pass

    @property
    @abstractmethod
    def temperature(self):
        """return the temperature values of (collection of) sondes"""
        pass

    @property
    @abstractmethod
    def dewpoint(self):
        """return the dewpoint values of (collection of) sondes"""
        pass

    @property
    @abstractmethod
    def relative_humidity(self):
        """return the relative humidity values of (collection of) sondes"""
        pass

    @property
    @abstractmethod
    def wind_speed(self):
        """return the horizontal wind speed values of (collection of) sondes"""
        pass

    @property
    @abstractmethod
    def wind_direction(self):
        """return the horizontal wind direction values of (collection of) sondes"""
        pass

    @property
    @abstractmethod
    def wind_east(self):
        """return the eastern component of wind speed values of (collection of) sondes"""
        pass

    @property
    @abstractmethod
    def wind_north(self):
        """return the northern component of wind speed values of (collection of) sondes"""
        pass

class BaseRadiosonde(BaseRadiosondeComponent):

    def __init__(self, launch_lat, launch_lon, launch_time) -> None:

        gps = GeoLocation(lat=launch_lat, lon=launch_lon)
        time = SondeDatetime.from_datetime(launch_time)
        self._launch_info = LaunchInfo(launch_time=time,
                                       launch_gps=gps) 

    def is_list(self) -> bool:
        return False

    @property
    def launch_lat(self):
        return self._launch_info['launch_gps'].lat

    @property
    def launch_lon(self):
        return self._launch_info['launch_gps'].lon

    @property
    def launch_gps(self):
        return self._launch_info['launch_gps']

    @property
    def launch_time(self):
        return self._launch_info['launch_time']

    def some_operation(self) -> str:

        return "This is a BaseRadiosonde"

class BaseRadiosondeList(BaseRadiosondeComponent):
    """Composite for Radiosondes"""

    def __init__(self) -> None:
        self._children = []

    def __len__(self) -> int:
        return len(self._children)

    def add(self, radiosonde: BaseRadiosonde) -> None:
        self._children.append(radiosonde)

    def extend(self, radiosonde_list: BaseRadiosondeList) -> None:
        self._children.extend(radiosonde_list._children)
        
    def remove(self, radiosonde: BaseRadiosonde) -> None:
        self._children.remove(radiosonde)

    def is_list(self) -> bool:
        return True

    def some_operation(self) -> str:

        return "This is a BaseRadiosodneList"
