from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtProperty, pyqtSignal, QModelIndex

from libraries.dataLoader.pandas_loader import pandas_loader
from libraries import helpers
from interface.core_table_widget import utilities
import settings


class DataFrameTableModel(QAbstractTableModel):
    """custom model for the core table view
    """
    def __init__(self, data_file_info_obj):
        super().__init__()
        self.loadData(data_file_info_obj)

    def loadData(self, data_file_info_obj):
        preview_mode = data_file_info_obj['preview_mode']
        args = data_file_info_obj['file'].get_all_properties(preview_mode=preview_mode)
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
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self.df_data.iat[index.row(), index.column()])
    
    def flags(self, index):
        """all columns are currently selectable and editable"""
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        column_header = self.df_data.columns[column]
        self.df_data.sort_values(by=column_header, inplace=True, ascending=order==Qt.AscendingOrder)
        self.layoutChanged.emit()

    def removeColumns(self, columns):
        """Remove columns.
        Args:
            columns(list): A list of column headers
        """
        column_indexes = utilities.pop_elements_index(columns, self.columns)
        for i, column_index in enumerate(column_indexes):
            self.beginRemoveColumns(QModelIndex(), column_index, column_index)
            self.df_data.drop(labels=columns[i], axis=1, inplace=True)
            self.endRemoveColumns()


if __name__ == "__main__":
    df_model = DataFrameTableModel()