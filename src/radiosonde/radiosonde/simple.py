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
        return self._data.loc[:,'humidity'].values
    
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
