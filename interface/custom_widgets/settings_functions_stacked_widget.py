from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QFileDialog
from PyQt5.QtCore import pyqtSignal
from interface.custom_widgets.ui_settings_functions_stacked_widget import Ui_StackedWidget
from libraries.dataLoader.utilities import parse_data_format_from_path
import settings

class SettingsFunctionsStackedWidget(QStackedWidget,Ui_StackedWidget):
    csv_path_entered_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.num_stack_pages = 0
        self.path = ''
        self.setupUi(self)
        self.resize(0,0)

    def parse_path_slot(self):
        if self.path != self.path_le.text():
            parse_res = parse_data_format_from_path(self.path_le.text(), settings.SUPPORTED_DATA_FORMAT)
            if parse_res['result']:
                self.path = self.path_le.text()
                if parse_res['result'] == '.csv' or parse_res['result'] == '.tsv':
                    self.csv_path_entered_signal.emit(parse_res['result'])

            else:
                print(parse_res['warning'])

    def add_path_slot(self):
        path = QFileDialog.getOpenFileName(self, "Choose a file", "./", "All(*.*);;CSV(*.csv, *.tsv);;JSON(*.json)", "All(*.*)")[0]
        self.path_le.setText(path)

