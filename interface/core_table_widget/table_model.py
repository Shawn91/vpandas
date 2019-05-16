import sys
import os

from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtProperty
import pandas as pd

from libraries.dataLoader.pandas_loader import pandas_loader
import settings

class DataFrameTableModel(QAbstractTableModel):
    """custom model for the core table view
    
    Args:
        path(dataframe or str): A pandas dataframe or path to data source
        data_format(str, optional): ligit values are `csv`, `tsv`, `json`, etc. 
            Defaults to None and it could be inferred automatically, so generally there is no need to specify the value.
            For more info on this parameter, see ``pandasLoader``.
    """
    def __init__(self, data_file_info_obj):
        super().__init__()
        self.loadData(data_file_info_obj)

    def loadData(self, data_file_info_obj):
        args = data_file_info_obj.get_all_properties()
        self.df_data = pandas_loader.load_data(path=args['path'], data_format=args['data_format'], encoding=args['encoding'],
                                               sample_size=args['sample_size'], sample_method=args['sample_method'],
                                               sep=args['sep'], header_line=args['header_line'], record_num=args['record_num']['estimated'])['result']
    
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
    df_model = DataFrameTableModel()