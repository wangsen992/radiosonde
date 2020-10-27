from abc import ABC, abstractmethod

from ..internals.launch_info import LaunchInfo
from ..internals.data_info import DataInfo

class BaseRadiosondeComponent(ABC):
    """Define an interface for working with radiosonde data"""

    def __init__(self) -> None:
        self.launch_info : LaunchInfo = {}
        self.data_info   : DataInfo = DataInfo()

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

    def is_list(self) -> bool:
        return False

    def some_operation(self) -> str:

        return "This is a BaseRadiosonde"

class BaseRadiosondeList(BaseRadiosondeComponent):
    """Composite for Radiosondes"""

    def __init__(self) -> None:
        self._children = []

    def add(self, radiosonde: BaseRadiosondeComponent) -> None:
        self._children.append(radiosonde)
        
    def remove(self, radiosonde: BaseRadiosondeComponent) -> None:
        self._children.remove(radiosonde)

    def is_list(self) -> bool:
        return True

    def some_operation(self) -> str:

        return "This is a BaseRadiosodneList"
