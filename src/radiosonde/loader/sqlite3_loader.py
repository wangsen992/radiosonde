import sqlite3
import pandas as pd
from .base_loader import BaseSondeLoader
from ..radiosonde.simple import SimpleDataFrameRadiosonde as Radiosonde
from ..utils.datetime.sqlite3 import SQLite3Datetime as datetime

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
            t_range = (datetime.fromisoformat(criteria['t_range'][0]),\
                      datetime.fromisoformat(criteria['t_range'][1]))
            if criteria.get('z_range') is not None:
                where_query += f"and LaunchTime between '{t_range[0]}' and '{t_range[1]}' " 
            else:
                where_query = f"where LaunchTime between '{t_range[0]}' and '{t_range[1]}' " 
        group_query =  "group by LaunchTime, Dropping"

        allsondes = pd.read_sql(sql=select_query+where_query+group_query,
                                con=self.conn,
                                parse_dates=['LaunchTime','startTime', 'endTime'])
        allsondes['startTime'] = allsondes['startTime'].dt.tz_localize(None)
        allsondes['endTime'] = allsondes['endTime'].dt.tz_localize(None)
        allsondes['LaunchTime'] = allsondes['LaunchTime'].dt.tz_localize(None)
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
        """Load radiosonde data (multiple) from sqlite3 database"""
        self.__open_connection()
        sql_query = f"select * from sonde where LaunchTime='{launchtime}'"
        out = pd.read_sql(sql_query, 
                          self.conn, 
                          parse_dates=['timestamp'])
        self.__close_connection()
        rds = Radiosonde(df=out)
        return  rds
