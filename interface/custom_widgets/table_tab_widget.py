from PyQt5.QtWidgets import QTabWidget

from interface.core_table_widget.table_model import DataFrameTableModel
from interface.custom_widgets.ui_table_tab_widget import Ui_TabWidget
from interface.core_table_widget import table_delegates
from libraries import helpers
import settings

class TableTabWidget(QTabWidget, Ui_TabWidget):
    """A custom QTabWidget with size hint of (1,1) instead of the default (6,6) to make make a proper layout"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)  # set up UI created by Qt Designer
        self.init_ui() # set up UI programmatically

    def init_ui(self):
        self.dataframe_table_view.setAlternatingRowColors(True)
        self.dataframe_table_view.selectionModel()
        self.dataframe_table_view.setItemDelegate(table_delegates.InLineEditDelegate())

    @helpers.MyPyQtSlot()
    def load_table(self, data_file_info_obj):
        df_model = DataFrameTableModel(data_file_info_obj)
        self.dataframe_table_view.setModel(df_model)

