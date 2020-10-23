from abc import ABC, abstractmethod

from ..internals.launch_info import LaunchInfo
from ..internals.data_info import DataInfo

class BaseRadiosondeComponent(ABC):
    """Define an interface for working with  radiosonde data"""

    def __init__(self) -> None:
        self.launch_info : LaunchInfo = {}
        self.data_info   : DataInfo = DataInfo()

    def is_list(self) -> bool:
        
        return False

    @abstractmethod
    def some_operation(self)  -> str:
        """Defines the interface here"""
        pass

class BaseRadiosonde(BaseRadiosondeComponent):

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
