from PyQt5.QtWidgets import QWidget,QStackedWidget,QSplitter,QHBoxLayout,QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from interface.custom_widgets.table_tab_widget import TableTabWidget
from interface.custom_widgets.settings_functions_stacked_widget import SettingsFunctionsStackedWidget
from interface.custom_widgets.info_stacked_widget import InfoStackedWidget
import settings

class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.init_ui()
        self.handle_signals()

    def init_ui(self):
        hlayout = QHBoxLayout()

        self.settings_functions_stacked_widget = SettingsFunctionsStackedWidget()
        settings_content_splitter = QSplitter(Qt.Horizontal)

        table_info_splitter = QSplitter(Qt.Vertical)
        self.table_tab_widget = TableTabWidget()
        self.info_stacked_widget = InfoStackedWidget()
        table_info_splitter.addWidget(self.table_tab_widget)
        table_info_splitter.addWidget(self.info_stacked_widget)

        # The two numbers 20000 and 10000 indicate the relative sizes of the two child widgets.
        # The numbers are purposely set very big instead of 2 and 1.
        # See https://stackoverflow.com/questions/29560912/qsplitter-stretching-factors-behave-differnt-from-normal-ones for reference
        table_info_splitter.setSizes([20000,10000])
        settings_content_splitter.addWidget(self.settings_functions_stacked_widget)
        settings_content_splitter.addWidget(table_info_splitter)
        settings_content_splitter.setSizes([10000, 40000])
        hlayout.addWidget(settings_content_splitter)
        self.setLayout(hlayout)

        self.settings_functions_stacked_widget.setFrameShape(QFrame.StyledPanel)
        self.info_stacked_widget.setFrameShape(QFrame.StyledPanel)

    def handle_signals(self):
        self.settings_functions_stacked_widget.data_load_ready_signal.connect(self.table_tab_widget.load_table)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication,QMainWindow
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.resize(1920,1080)
    centralWidget = CentralWidget()
    window.setCentralWidget(centralWidget)
    window.show()
    sys.exit(app.exec_())
