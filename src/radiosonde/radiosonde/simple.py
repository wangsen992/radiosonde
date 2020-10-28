import pandas as pd
from .base import BaseRadiosonde, BaseRadiosondeList
# Try to replace direct dependency on metpy
from metpy.units import units

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

