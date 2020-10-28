from datetime import datetime
from siphon.simplewebservice import igra2
from importlib_resources import path

import pandas as pd
import pint

from ..base_loader import BaseSondeLoader
from ...radiosonde import  Radiosonde
from ...radiosonde import  RadiosondeList
# Try to replace direct dependency on metpy


class Igra2SondeLoader(BaseSondeLoader):

    def __init__(self, site_id='CAM00071802'):
        self.conn = igra2.IGRAUpperAir()
        self.__site_id = site_id
        with path(__package__, 'igra2-country-list.txt') as p:
            self.country_list = pd.read_fwf(p, names=['code','full'])

        with path(__package__, 'igra2-station-list.txt') as p:
            self.station_list = pd.read_fwf(p,
                    names=['site_id','lat','lon','alt','name','first_year',
                    'end_year', 'tot_release']).set_index('site_id')
    @property
    def site_id(self):
        return self.__site_id
    @site_id.setter
    def site_id(self, site_id_string):
        if site_id_string in self.station_list.index:
            self.__site_id = site_id_string
        else:
            raise KeyError("input id is not in station list")
    @property
    def site_name(self):
        return self.station_list.loc[self.site_id, 'name']

    def load_one(self, launchtime):
        """Load one radiosonde into the required format. 

        Arguments:
            launchtime (datetime.datetime): launch time of sonde
            site_id (str) : station code
        """

        ret_data = self.conn.request_data(site_id = self.site_id,
                                          time  = launchtime)
        launch_lat = ret_data[1]['latitude'].values[0]
        launch_lon = ret_data[1]['longitude'].values[0]
        launch_time = launchtime

        out_tmp = ret_data[0]
        out  = pd.DataFrame({
            "height" : pd.Series(out_tmp['height'], dtype="pint[m]"),
            "pressure" : pd.Series(out_tmp['pressure'], dtype="pint[hPa]"),
            "temperature" : pd.Series(out_tmp['temperature'], dtype="pint[degC]"),
            "dewpoint" : pd.Series(out_tmp['dewpoint'], dtype="pint[degC]"),
            "relative_humidity" : pd.Series(out_tmp['relative_humidity'], dtype="pint[dimensionless]"),
            "wind_speed" : pd.Series(out_tmp['speed'], dtype="pint[m/s]"),
            "wind_direction" : pd.Series(out_tmp['direction'], dtype="pint[deg]"),
            "wind_east" : pd.Series(out_tmp['u_wind'], dtype="pint[m/s]"),
            "wind_north" : pd.Series(out_tmp['v_wind'], dtype="pint[m/s]"),
            })
        rds = Radiosonde(df = out, 
                         launch_lat = launch_lat,
                         launch_lon = launch_lon,
                         launch_time = launch_time)
        return rds

