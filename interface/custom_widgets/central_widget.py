from PyQt5.QtWidgets import QWidget,QStackedWidget,QSplitter,QHBoxLayout,QFrame
from PyQt5.QtCore import Qt

from interface.custom_widgets.table_tab_widget import TableTabWidget
from interface.custom_widgets.settings_functions_stacked_widget import SettingsFunctionsStackedWidget
from interface.custom_widgets.info_stacked_widget import InfoStackedWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.init_ui()

    def init_ui(self):
        hlayout = QHBoxLayout()

        settings_functions_stacked_widget = SettingsFunctionsStackedWidget()
        settings_content_splitter = QSplitter(Qt.Horizontal)

        table_info_splitter = QSplitter(Qt.Vertical)
        table_tab_widget = TableTabWidget()
        info_stacked_widget = InfoStackedWidget()
        table_info_splitter.addWidget(table_tab_widget)
        table_info_splitter.addWidget(info_stacked_widget)
        table_info_splitter.setStretchFactor(0, 3)
        table_info_splitter.setStretchFactor(1, 1)

        settings_content_splitter.addWidget(settings_functions_stacked_widget)
        settings_content_splitter.addWidget(table_info_splitter)
        settings_content_splitter.setStretchFactor(0, 1)
        settings_content_splitter.setStretchFactor(1, 4)
        hlayout.addWidget(settings_content_splitter)
        self.setLayout(hlayout)

        settings_functions_stacked_widget.setFrameShape(QFrame.StyledPanel)
        info_stacked_widget.setFrameShape(QFrame.StyledPanel)


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
