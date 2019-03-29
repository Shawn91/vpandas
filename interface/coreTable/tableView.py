import sys

from PyQt5 import Qt



class DataTableView(Qt.QTableView):
    def __init__(self, r=3,c=3):
        super().__init__(r,c)


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)

    class Sheet(Qt.QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent=parent)

            self.form_widget = DataTableView(10 ,10)

            # central widget 可以理解为一个窗口除了标题栏状态栏等之外的主要功能区（使用一个 widget 占据）
            self.setCentralWidget(self.form_widget)
        
    v = Sheet()
    v.show()
    sys.exit(app.exec_())