"""GPS datastructure as an interface for other capabilities"""

class GeoLocation:

    def __init__(self, lat, lon):
        self.__lat = lat
        self.__lon = lon

    @property
    def lat(self):
        return self.__lat

    @property
    def lon(self):
        return self.__lon

    def to_tuple(self):
        return self.__lat, self.__lon

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__lat}, {self.__lon})"
