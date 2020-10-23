import pandas as pd


class DataInfo(pd.DataFrame):
    """DataFrame containing the radiosonde data values without unit support"""
    def __init__(self, 
                 timestamp   = None,
                 pressure    = None, 
                 temperature = None, 
                 humidity    = None, 
                 windDir     = None,
                 windSpeed   = None,
                 altitude    = None,
                 gps         = None) -> None:
        """Constructor requires input of the most essential variables."""
        pass
