import sqlite3
from datetime import datetime
import pandas as pd
import pint

from ..base_loader import BaseSondeLoader
from ...radiosonde import  Radiosonde
from ...radiosonde import  RadiosondeList
from .sqlite3_datetime import SQLite3Datetime as SondeDatetime
# Try to replace direct dependency on metpy
from metpy.units import units
from metpy import calc

class SQLite3SondeLoader(BaseSondeLoader):

    def __open_connection(self):
        self.conn = sqlite3.connect(self.filepath)

    def __close_connection(self):
        self.conn.close()

    def list_vars(self):
        pass

    def available(self, criteria :  dict):
        """Show available sondes based on criterion

        Criterion available:
            z_range (tuple[float, float]) : the min and max altitude, z_range
                must be positive and increasing in value. 
            t_range (tuple[str, str]) : the start and  end time bound for
                radiosonde launchtimes
            pct (float) : percentage of data availble for the given height
                range. Condition: 0 < pct < 1.0
        """
        assert self._is_criteria_valid(), "Criteria not valid"
        self.__open_connection()

        select_query = "select LaunchTime, "\
                   + "min(timestamp) as startTime, max(timestamp) as endTime, "\
                   + "min(Height) as minHeight, max(Height) as maxHeight, "\
                   + "avg(Latitude) as Latitude, avg(Longitude) as Longitude,"\
                   + "min(Dropping) as dropping "\
                   + "from sonde "
        where_query = ""
       
        if criteria.get('z_range') is not None:
            z_range = criteria['z_range']
            where_query = f"where Height between {z_range[0]} and {z_range[1]} "\

        if criteria.get('t_range') is not None:
            t_range = (SondeDatetime.fromisoformat(criteria['t_range'][0]),\
                      SondeDatetime.fromisoformat(criteria['t_range'][1]))
            if criteria.get('z_range') is not None:
                where_query += f"and LaunchTime between '{t_range[0]}' and '{t_range[1]}' " 
            else:
                where_query = f"where LaunchTime between '{t_range[0]}' and '{t_range[1]}' " 
        group_query =  "group by LaunchTime, Dropping"

        allsondes = pd.read_sql(sql=select_query+where_query+group_query,
                                con=self.conn)
        if criteria.get('z_range') is not None and criteria.get('pct') is not None:
            pct = criteria['pct']
            out =  allsondes.query('(maxHeight - minHeight)/{z_full} > {pct}'\
                                   .format(z_full=z_range[1]-z_range[0],pct=pct))\
                                   .reset_index(drop=True)
        else:
            out = allsondes.reset_index(drop=True)

        self.__close_connection()
        return out

    def load(self, start, end):

        pass

    def load_one(self, launchtime, dropping=0):
        """Load radiosonde data (multiple) from sqlite3 database

        Argumets:
            launchtime (str) : exact string method obtained from available
            method.
            dropping (int) : 0 for ascending, 1 or dropping
        """
        self.__open_connection()
        sql_query = f"select * from sonde where LaunchTime='{launchtime}' and Dropping={dropping}"
        rename_dict = {"Altitude" : "height",
                       "Pressure"  : "pressure",
                       "Temperature" : "temperature",
                       "Humidity"  : "relative_humidity",
                       "WindSpeed" : "wind_speed",
                       "WindDir" :  "wind_direction",
                       "WindEast" : "wind_east",
                       "WindNorth" : "wind_north"}
        out_tmp = pd.read_sql(sql_query, 
                          self.conn, 
                          index_col='timestamp',
                          parse_dates=['timestamp']).rename(columns=rename_dict)
        self.__close_connection()

        # convert to united dataframe with pint
        out  = pd.DataFrame({
            "height" : pd.Series(out_tmp['height'], dtype="pint[m]"),
            "pressure" : pd.Series(out_tmp['pressure'], dtype="pint[hPa]"),
            "temperature" : pd.Series(out_tmp['temperature'], dtype="pint[kelvin]"),
            "relative_humidity" : pd.Series(out_tmp['relative_humidity']/100, dtype="pint[dimensionless]"),
            "wind_speed" : pd.Series(out_tmp['wind_speed'], dtype="pint[m/s]"),
            "wind_direction" : pd.Series(out_tmp['wind_direction'], dtype="pint[deg]"),
            "wind_east" : pd.Series(out_tmp['wind_east'], dtype="pint[m/s]"),
            "wind_north" : pd.Series(out_tmp['wind_north'], dtype="pint[m/s]"),
            })

        temperature = out['temperature'].values.data * units('kelvin')
        rh = out['relative_humidity'].values.data * units('dimensionless')
        dewpoint = calc.dewpoint_from_relative_humidity(temperature, rh)\
                       .to('kelvin') # needed for slicing. prolem with degC as
        out['dewpoint'] = pd.Series(dewpoint.m, dtype=f"pint[{str(dewpoint.units)}]")
        # a dirty adaptor to load the radiosonde into  the required format
        time,_, micro_secs = launchtime[:-4].rpartition('.')
        if len(micro_secs) < 6:
            micro_secs += '0' * (6 - len(micro_secs))
            launchtime = time  + '.' + micro_secs + " UTC"
        if dropping == 0:
            launch_time = datetime.fromisoformat(launchtime[:-4])
            launch_lat = out_tmp['LaunchLatitude'].values[0]
            launch_lon = out_tmp['LaunchLongitude'].values[0]
        elif dropping == 1:
            launchtime_tmp = out_tmp.index.max()
            launch_time = launchtime_tmp.to_pydatetime()
            launch_lat = out_tmp.loc[launchtime_tmp,'Latitude']
            launch_lon = out_tmp.loc[launchtime_tmp,'Longitude']
        rds = Radiosonde(df=out,
                         launch_lat = launch_lat,
                         launch_lon = launch_lon,
                         launch_time = launch_time)
        return  rds

    def load_many(self, launchtime_list, dropping=0, verbose=True):
        """Overwrite load_many from base class"""

        sondeList =  RadiosondeList()
        for time  in launchtime_list:
            try: 
                sonde = self.load_one(time, dropping=dropping)
                sondeList.add(sonde)
                print(f"Sonde at {sonde.launch_time} downloaded succesfully")
            except:
                print(f"[Error] Somethign went wrong for {time}. Skipped...")
        return sondeList
