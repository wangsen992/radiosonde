import sqlite3
from .base import BaseDatetime

class SQLite3Datetime(BaseDatetime):

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.strftime("%Y-%m-%d %H:%M:%S.%f UTC")

    def to_str(self):
        return self.strftime("%Y-%m-%d %H:%M:%S.%f UTC")



if __name__ == "__main__":
    sd = SQLite3Datetime(2018, 9, 13, 15)
