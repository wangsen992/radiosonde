from datetime import datetime

class BaseDatetime:
    """Base Datetime class for common interface dealing with diffferent file
    formats."""
    
    # Constructor
    def __init__(self, year, month, day, hour=0, minute=0, second=0,
            microsecond=0, tzinfo=None, *, fold=0):
        """Init with the same constructor as datetime.datetime"""

        self.__datetime =   datetime(year=year, 
                                     month=month,
                                     day=day,
                                     hour=hour,
                                     minute=minute,
                                     second=second,
                                     microsecond=microsecond,
                                     tzinfo=tzinfo,
                                     fold=fold)
    # property method
    @property
    def year(self):
        return self.__datetime.year

    @property
    def month(self):
        return self.__datetime.month
    @property
    def day(self):
        return self.__datetime.day
    @property
    def hour(self):
        return self.__datetime.hour
    @property
    def minute(self):
        return self.__datetime.minute
    @property
    def second(self):
        return self.__datetime.second
    @property
    def microsecond(self):
        return self.__datetime.microsecond
    @property
    def tzinfo(self):
        return self.__datetime.tzinfo
    @property
    def fold(self):
        return self.__datetime.fold

    @classmethod
    def from_datetime(cls, dt):
        """Convert from datetime.datetime"""

        return cls(year=dt.year, 
                             month=dt.month,
                             day=dt.day,
                             hour=dt.hour,
                             minute=dt.minute,
                             second=dt.second,
                             microsecond=dt.microsecond,
                             tzinfo=dt.tzinfo,
                             fold=dt.fold)



    @classmethod
    def fromisoformat(cls, date_string):
        """Adaptor to use datetime.datetime.fromisoformat(date_string)"""
        return cls.from_datetime((datetime.fromisoformat(date_string)))

    # Instance Methods
    def isoformat(self, sep='T', timespec='auto'):
        """Adaptor to use datetime.datetime.isoformat() method"""
        return self.__datetime.isoformat(sep=sep, timespec=timespec)

    def strftime(self, format):
        """Adaptor to use datetime.datetime.strftime() method"""
        return self.__datetime.strftime(format)


    def __repr__(self):
        return """{cls_name}({dt.year}, {dt.month}, {dt.day}, {dt.hour}, {dt.minute}, {dt.second}, {dt.microsecond}, tzinfo={dt.tzinfo})""".format(cls_name=self.__class__.__name__, dt=self.__datetime)

if __name__ == '__main__':
    bd = BaseDatetime.fromisoformat("2018-09-03 23:11:31.625282+00:00")
