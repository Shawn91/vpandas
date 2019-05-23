from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QFileDialog
from PyQt5.QtCore import pyqtSignal


from interface.custom_widgets.ui_settings_functions_stacked_widget import Ui_StackedWidget
from libraries.dataLoader.data_file_info import DataFileInfo
import settings
from libraries import helpers

# TODO: random seed function


class SettingsFunctionsStackedWidget(QStackedWidget, Ui_StackedWidget):
    data_load_ready_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.num_stack_pages = 0
        self.file = DataFileInfo()
        self.setupUi(self) # set up UI created by Qt Designer
        self.init_ui() # set up UI programmatically
        self.field_widgets = {'encoding':self.encoding_le, 'size':self.size_le, 'size_unit':self.size_label,
                'estimated_record_num':self.record_num_label, 'exact_record_num':self.record_num_label,
                'sep':self.csv_seperator_le, 'header_line':self.csv_header_le
        }

    def init_ui(self):
        self.csv_settings_widget.setEnabled(False)
        self.random_seed_wcontainer.setVisible(False)

    @helpers.MyPyQtSlot()
    def parse_path_slot(self, changed_text):
        if self.file.path != self.path_le.text():
            self.file.path = self.path_le.text()
            self.populate_fields_warnings()

    @helpers.MyPyQtSlot()
    def add_path_slot(self, clicked):
        path = QFileDialog.getOpenFileName(self, "Choose a file", "./", "All(*.*);;CSV(*.csv, *.tsv);;JSON(*.json)", "All(*.*)")[0]
        self.path_le.setText(path)

    @helpers.MyPyQtSlot()
    def populate_fields_warnings(self):
        self.path_warning_label.setText(self.file.warnings.get('path',''))
        if not self.file.warnings.get('path'):
            self.load_data_btn.setEnabled(True)
            self.data_load_ready_signal.emit({'file':self.file, 'preview_mode':True})
        self.file.delete_warning('path')

        for field, value in self.file.get_all_properties().items():
            if field in ['path', 'headers', 'sample_size', 'sample_method']:
                continue

            if field == 'data_format':
                if value in ('.csv', '.tsv'):
                    self.csv_settings_widget.setEnabled(True)
                else:
                    self.csv_settings_widget.setEnabled(False)
                continue

            if field == 'record_num':
                if value['exact']:
                    self.record_num_label.setText(str(value['exact']))
                else:
                    self.record_num_label.setText(str(value['estimated']) + ' (estimated)')
                continue

            self.field_widgets[field].setText(str(value))

    @helpers.MyPyQtSlot()
    def load_data_slot(self, clicked):
        self.collect_file_info()
        self.data_load_ready_signal.emit({'file' : self.file, 'preview_mode' : False})

    @helpers.MyPyQtSlot()
    def load_test_data_slot(self, clicked):
        self.path_le.setText('E:/Study/microsoft-malware-prediction/train.csv')

    @helpers.MyPyQtSlot()
    def show_random_seed_wcontainer_slot(self, selected_item):
        if selected_item == 'random':
            self.random_seed_wcontainer.setVisible(True)
        else:
            self.random_seed_wcontainer.setVisible(False)

    @helpers.MyPyQtSlot()
    def collect_file_info(self):
        self.file.path = self.path_le.text()
        self.file.encoding = self.encoding_le.text()
        self.file.size = (self.size_le.text(), self.size_label.text())
        self.file.sep = self.csv_seperator_le.text()
        self.file.header_line = self.csv_header_le.text()
        self.file.sample_method = self.sample_method_cmbbox.currentText()
        self.file.sample_size = self.sample_size_le.text()

    def select_columns_slot(self, clicked):
        pass
