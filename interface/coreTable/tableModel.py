import sys
import os

# from PyQt5.Qt import *
from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtProperty
import pandas as pd

from libs.dataLoader.pandasLoader import pandas_loader

class DataFrameTableModel(QAbstractTableModel):
    """custom model for the core table view
    
    Args:
        df_data_path(dataframe or str): A pandas dataframe or path to data source
        data_format(str, optional): ligit values are `csv`, `tsv`, `json`, etc. 
            Defaults to None and it could be inferred automatically, so generally there is no need to specify the value.
            For more info on this parameter, see ``pandasLoader``.
    """
    def __init__(self, df_data_path, data_format=None):
        super().__init__()
        self.df_data = self.loadData(df_data_path=df_data_path,data_format=data_format)

    
    def loadData(self, df_data_path=None, data_format=None, **kwargs):
        if df_data_path:
            if isinstance(df_data_path, pd.core.frame.DataFrame):
                return df_data_path
            if isinstance(df_data_path, str):
                return pandas_loader.load_data(path=df_data_path, data_format=data_format,**kwargs)
        else:
            raise ValueError("df_data_path must be a pandas dataframe or path to the data but received a %s" % type(df_data_path))
    
    @pyqtProperty(list)
    def columns(self):
        return list(self.df_data.columns)
    
    def rowCount(self, *args, **kwargs):
        return self.df_data.shape[0]
    def columnCount(self, *args, **kwargs):
        return self.df_data.shape[1]
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """currently only support horizontal headers"""
        if orientation==Qt.Horizontal and role==Qt.DisplayRole:
            return self.columns[section]
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self.df_data.iat[index.row(), index.column()])
    
    def flags(self, index):
        """all columns are currently selectable and editable"""
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
    # def setData(self, )
    



if __name__ == "__main__":
    df_model = DataFrameTableModel([1])