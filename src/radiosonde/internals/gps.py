"""GPS datastructure as an interface for other capabilities"""

class GeoLocation:

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __repr(self):
        return f"{self.__class__.__name__}({self.lat}, {self.lon})"
