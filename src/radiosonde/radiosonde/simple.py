import pandas as pd
from .base import BaseRadiosonde, BaseRadiosondeList
# Try to replace direct dependency on metpy
from metpy.units import units

__all__ = ["SimpleDataFrameRadiosonde", "SimpleDataFrameRadiosondeList"]

class SimpleDataFrameRadiosonde(BaseRadiosonde):
    """A simple inheritance of pd.DataFrame"""

    def __init__(self, df, launch_lat, launch_lon, launch_time):
        BaseRadiosonde.__init__(self, 
                                launch_lat=launch_lat, 
                                launch_lon=launch_lon, 
                                launch_time=launch_time)
        self._data = df

    def some_operation(self):
        print("Do some operation here")

    # Variable accessor methods
    @property
    def height(self):
        return self._data.loc[:,'height'].values.data * \
        units(str(self._data['height'].values.units))

    @property
    def pressure(self):
        return self._data.loc[:,'pressure'].values.data * \
        units(str(self._data['pressure'].values.units))


    @property
    def temperature(self):
        return self._data.loc[:,'temperature'].values.data * \
        units(str(self._data['temperature'].values.units))


    @property
    def dewpoint(self):
        return self._data.loc[:,'dewpoint'].values.data * \
        units(str(self._data['dewpoint'].values.units))

    @property
    def relative_humidity(self):
        # Convert RH to between 0 and 1
        return self._data.loc[:,'relative_humidity'].values.data* \
        units(str(self._data['relative_humidity'].values.units))

    
    @property
    def wind_speed(self):
        return self._data.loc[:,'wind_speed'].values.data * \
        units(str(self._data['wind_speed'].values.units))


    @property
    def wind_direction(self):
        return self._data.loc[:,'wind_direction'].values.data * \
        units(str(self._data['wind_direction'].values.units))


    @property
    def wind_east(self):
        return self._data.loc[:,'wind_east'].values.data * \
        units(str(self._data['wind_east'].values.units))


    @property
    def wind_north(self):
        return self._data.loc[:,'wind_north'].values.data * \
        units(str(self._data['wind_north'].values.units))

class SimpleDataFrameRadiosondeList(BaseRadiosondeList):

    def __init__(self):
        BaseRadiosondeList.__init__(self)

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

