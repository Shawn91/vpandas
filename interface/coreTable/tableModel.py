import sys
import os

from PyQt5.Qt import *
import pandas as pd

from libs.dataLoader import pandasLoader

class DataFrameTableModel(QAbstractTableModel):
    """custom model for core table view
    
    Args:
        df_data: a pandas dataframe or None; you could load data later using `load_data` method.
    """
    def __init__(self, df_data=None):
        super().__init__()
        self.load_data(df_data)
    
    def load_data(self, df_data):
        if df_data:
            if isinstance(df_data, pd.core.frame.DataFrame):
                self.df_data = df_data
            if isinstance(df_data, str) and os.path.isfile(df_data):
                pass
        # raise IOError("Can't load the data passed to the model")


if __name__ == "__main__":
    # df_model = DataFrameTableModel([1])
    print(os.path.dirname(__file__))