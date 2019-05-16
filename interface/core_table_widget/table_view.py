import sys

from PyQt5 import Qt, QtWidgets

from interface.core_table_widget.table_model import DataFrameTableModel
import settings

class DataFrameTableView(Qt.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.selectionModel()

    def load_data(self, ):
        df_table_model = DataFrameTableModel()
        # self.setModel(df_table_model)

# class DataFrameTableWidget(Qt.QWidget):
#     def __init__(self, parent=None, df_data_path=None):
#         super().__init__(parent)
#         self.path = df_data_path
#         self.initUi()
#
#     def initUi(self):
#         self.tableView = DataFrameTableView(self)
#         self.tableView.setAlternatingRowColors(True)
#         self.tableView.setSortingEnabled(True)
#
#         self.tableView.selectionModel() # make table selectable
#         df_table_model = DataFrameTableModel()
#
#         # set layout
#         horizontalLayout = QtWidgets.QHBoxLayout()
#         horizontalLayout.setContentsMargins(0, 0, 0, 0)
#         self.setLayout(horizontalLayout)
#         horizontalLayout.addWidget(self.tableView)

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
        
    v = DataFrameTableWidget(df_data_path=r'E:\Study\projects\Wiki_Cities\2.csv')
    v.show()
    sys.exit(app.exec_())