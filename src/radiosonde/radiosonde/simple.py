import pandas as pd

class SimpleDataFrameRadiosonde(pd.DataFrame):
    """A simple inheritance of pd.DataFrame"""

    def __init__(self, df):
        pd.DataFrame.__init__(self, data=df)
        self.index.name = 'z'

