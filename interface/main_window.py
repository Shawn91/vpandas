import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from interface.custom_widgets.central_widget import CentralWidget

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        central_widget = CentralWidget()
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.resize(1920,1080)
    myWin.show()
    sys.exit(app.exec_())