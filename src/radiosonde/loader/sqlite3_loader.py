import sqlite3
import pandas as pd
from base_loader import BaseSondeLoader

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
            pct (float) : percentage of data availble for the given height
                range. Condition: 0 < pct < 1.0
        """
        self.__open_connection()
       
        if criteria.get('z_range') is None:
            sql_query = 'select distinct LaunchTime, LaunchLatitude, '\
                        + 'LaunchLongitude from sonde'
            out = pd.read_sql(sql_query, 
                              self.conn,
                              parse_dates=['LaunchTime'])

        else:
            sql_query = \
            "select min(timestamp) as startTime, max(timestamp) as endTime, "\
                   + "min(Height) as minHeight, max(Height) as maxHeight, "\
                   + "avg(Latitude) as Latitude, avg(Longitude) as Longitude,"\
                   + "min(Dropping) as dropping "\
               + "from sonde where Height between ? and ? "\
               + "group by LaunchTime, Dropping"
            allsondes = pd.read_sql(sql_query,
                                    conn,
                                    parse_dates=['startTime', 'endTime'],
                                    params=z_range)
            allsondes['startTime'] = allsondes['startTime'].dt.tz_localize(None)
            allsondes['endTime'] = allsondes['endTime'].dt.tz_localize(None)
            out =  allsondes.query('(maxHeight - minHeight)/{z_full} > {pct}'\
                                   .format(z_full=z_range[1]-z_range[0],pct=pct))\
                                   .reset_index(drop=True)

        self.__close_connection()
        return out

    def load(self, start, end):
        pass
