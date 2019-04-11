import sys

from PyQt5 import Qt, QtWidgets

from interface.coreTable.tableModel import DataFrameTableModel

class DataFrameTableView(Qt.QTableView):
    def __init__(self, parent=None):
        super().__init__()

class DataFrameTableWidget(Qt.QWidget):
    def __init__(self, parent=None, df_data_path=None):
        super().__init__(parent)
        self.path = df_data_path
        self.initUi()
    
    def initUi(self):
        self.tableView = DataFrameTableView(self)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)

        self.tableView.selectionModel() # make table selectable
        self.tableView.setModel(DataFrameTableModel(df_data_path=self.path))

        # set layout
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(horizontalLayout)
        horizontalLayout.addWidget(self.tableView)

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
        
    v = DataFrameTableWidget(df_data_path=r'E:\Study\projects\Wiki_Cities\2.csv')
    v.show()
    sys.exit(app.exec_())