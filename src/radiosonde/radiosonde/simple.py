import pandas as pd
from .base import BaseRadiosonde, BaseRadiosondeList

class SimpleDataFrameRadiosonde(BaseRadiosonde):
    """A simple inheritance of pd.DataFrame"""

    def __init__(self, df, launch_lat, launch_lon, launch_time):
        BaseRadiosonde.__init__(self, launch_lat, launch_lon, launch_time)
        self._data = df

    def some_operation(self):
        print("Do some operation here")

    # Variable accessor methods
    @property
    def height(self):
        return self._data.loc[:,'height'].values

    @property
    def pressure(self):
        return self._data.loc[:,'pressure'].values

    @property
    def temperature(self):
        return self._data.loc[:,'temperature'].values

    @property
    def dewpoint(self):
        raise  NotImplementedError("Dewpoint not available, need to load compute")

    @property
    def relative_humidity(self):
        # Convert RH to between 0 and 1
        return self._data.loc[:,'relative_humidity'].values / 100
    
    @property
    def wind_speed(self):
        return self._data.loc[:,'wind_speed'].values

    @property
    def wind_direction(self):
        return self._data.loc[:,'wind_direction'].values

    @property
    def wind_east(self):
        return self._data.loc[:,'wind_east'].values

    @property
    def wind_north(self):
        return self._data.loc[:,'wind_north'].values

class SimpleDataFrameRadiosondeList(BaseRadiosondeList):

    def __init__(self):
        BaseRadiosondeList.__init__(self)

    def is_list(self) -> bool:
        pass

    def some_operation(self)  -> str:
        """Defines the interface here"""
        pass

    # Variable accessors
    @property
    def height(self):
        """return the height values of (collection of) sondes"""
        pass

    @property
    def pressure(self):
        """return the pressure values of (collection of) sondes"""
        pass

    @property
    def temperature(self):
        """return the temperature values of (collection of) sondes"""
        pass

    @property
    def dewpoint(self):
        """return the dewpoint values of (collection of) sondes"""
        pass

    @property
    def relative_humidity(self):
        """return the relative humidity values of (collection of) sondes"""
        pass

    @property
    def wind_speed(self):
        """return the horizontal wind speed values of (collection of) sondes"""
        pass

    @property
    def wind_direction(self):
        """return the horizontal wind direction values of (collection of) sondes"""
        pass

    @property
    def wind_east(self):
        """return the eastern component of wind speed values of (collection of) sondes"""
        pass

    @property
    def wind_north(self):
        """return the northern component of wind speed values of (collection of) sondes"""
        pass

