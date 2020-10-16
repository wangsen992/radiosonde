from abc import abstractmethod

class BaseSondeLoader:
    """Base loader interface for radiosonde to define common loading
    interface

    To use: 
    >>> loader = SondeLoader(filepath=path)
    >>> loader.list_vars()
    ['U','UDir', 'z', 'p' ..]
    >>> loader.available()
    TODO: Some  representation of radiosonde here. 
    >>> loader.load(start='2018-09-13 11:00:00', '2018-09-13 20:00:00')
    TODO: Some  representation of radiosonde here. 
    """

    def __init__(self, filepath):
        """Init. 

        Args:
           filepath  (str) : filepath  or directory path (for list of files)
        """
        self.filepath = filepath

    @abstractmethod
    def list_vars(self):
        """Return a list of available parameters in the given source

        TODO: There should be a check to ensure uniformity of all files. 

        Returns: 
            list[str] : variables names
        """
        assert self.__is_var_uniform(), "varaibles needs to be uniform"

    @abstractmethod
    def __is_var_uniform(self):
        """Check if variables names across files are the same. 

        Note: 
            To implement, make sure clear criteria is sticked to.
        """

        return True

    @abstractmethod
    def available(self,  criteria : dict):
        """Peek first understand available radiosondes based on certain criteria. 

        Args:
            criteria (dict) : dictionary for criteria when testing radiosonde
            data

        Notes: 
            criteria is arbitrary based on the available vars and data format
            (for recursing into all files). Specific implementation is
            required. 
        """
        pass

    @abstractmethod
    def load(self, start, end):
        """Abstract interface for radiosonde loader

        Args:
           start, end (str) : iso_format timestring used for bounding soundes. 

        Returns: 
            Radiosonde : The composite type of radiosonde collections. 
        """
        pass

def available(conn, z_range=None, pct=0.8):
    """List availble radiosondes from the sqlite3 database"""

    if z_range is None:
        sql_query = 'select distinct LaunchTime, LaunchLatitude, '\
                    + 'LaunchLongitude from sonde'
        return pd.read_sql(sql_query,
                           conn,
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
        return allsondes.query('(maxHeight - minHeight)/{z_full} > {pct}'\
                               .format(z_full=z_range[1]-z_range[0],pct=pct))\
                               .reset_index(drop=True)

def load(conn, meta, ddz_smooth_window=10):
    """Load radiosonde data (multiple) from sqlite3 database"""

    sql_query = "select * from sonde where timestamp between ? and ?"
    t_range = [meta['startTime'].strftime(iso_format),
               meta['endTime'].strftime(iso_format)]
    sonde_raw = pd.read_sql(sql_query,
                            conn,
                            parse_dates=['timestamp'],
                            params=t_range)
    sonde = sonde_raw[varsIncluded]
    return Radiosonde(sonde, meta, ddz_smooth_window)

