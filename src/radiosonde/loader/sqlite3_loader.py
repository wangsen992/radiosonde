import sqlite3
from datetime import datetime
import pandas as pd
from .base_loader import BaseSondeLoader
from ..radiosonde.simple import SimpleDataFrameRadiosonde as Radiosonde
from ..radiosonde.simple import SimpleDataFrameRadiosondeList as RadiosondeList
from ..internals.sonde_datetime.sqlite3 import SQLite3Datetime as SondeDatetime

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

    def load_one(self, launchtime):
        """Load radiosonde data (multiple) from sqlite3 database

        Argumets:
            launchtime (str) : exact string method obtained from available
            method.
        """
        self.__open_connection()
        sql_query = f"select * from sonde where LaunchTime='{launchtime}'"
        rename_dict = {"Altitude" : "height",
                       "Pressure"  : "pressure",
                       "Temperature" : "temperature",
                       "Humidity"  : "relative_humidity",
                       "WindSpeed" : "wind_speed",
                       "WindDir" :  "wind_direction",
                       "WindEast" : "wind_east",
                       "WindNorth" : "wind_north"}
        out = pd.read_sql(sql_query, 
                          self.conn, 
                          parse_dates=['timestamp'])
        self.__close_connection()

        # a dirty adaptor to load the radiosonde into  the required format
        time,_, micro_secs = launchtime[:-4].rpartition('.')
        if len(micro_secs) < 6:
            micro_secs += '0' * (6 - len(micro_secs))
            launchtime = time  + '.' + micro_secs + " UTC"
        launch_time = datetime.fromisoformat(launchtime[:-4])
        launch_lat = out['LaunchLatitude'].values[0]
        launch_lon = out['LaunchLongitude'].values[0]
        rds = Radiosonde(df=out.rename(columns=rename_dict),
                         launch_lat = launch_lat,
                         launch_lon = launch_lon,
                         launch_time = launch_time)
        return  rds

    def load_many(self, launchtime_list):

        sondeList =  RadiosondeList()
        for time  in launchtime_list:
            sondeList.add(self.load_one(time))
        return sondeList
