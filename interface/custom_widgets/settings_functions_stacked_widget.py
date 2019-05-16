from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QFileDialog
from PyQt5.QtCore import pyqtSignal


from interface.custom_widgets.ui_settings_functions_stacked_widget import Ui_StackedWidget
from libraries.dataLoader.utilities import parse_data_format_from_path,approximate_record_number,check_encoding
from libraries.dataLoader.data_file_info import DataFileInfo
import settings


class SettingsFunctionsStackedWidget(QStackedWidget,Ui_StackedWidget):
    data_load_ready_signal = pyqtSignal(object)


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


    def parse_path_slot(self, changed_text):
        if self.file.path != self.path_le.text():
            self.file.path = self.path_le.text()
            self.populate_fields_warnings()

    def add_path_slot(self):
        path = QFileDialog.getOpenFileName(self, "Choose a file", "./", "All(*.*);;CSV(*.csv, *.tsv);;JSON(*.json)", "All(*.*)")[0]
        self.path_le.setText(path)

    def populate_fields_warnings(self):
        self.path_warning_label.setText(self.file.warnings.get('path',''))
        if not self.file.warnings.get('path'):
            self.load_data_btn.setEnabled(True)
        self.file.delete_warning('path')


        for field, value in self.file.get_all_properties().items():
            if field in ['path','headers','sample_size','sample_method']:
                continue

            if field == 'data_format':
                if value in ('.csv', '.tsv'):
                    self.csv_settings_widget.setEnabled(True)
                else:
                    self.csv_settings_widget.setEnabled(False)
                continue

            if field  == 'record_num':
                if value['exact']:
                    self.record_num_label.setText(str(value['exact']))
                else:
                    self.record_num_label.setText(str(value['estimated'])+' (estimated)')
                continue
            self.field_widgets[field].setText(str(value))

    def load_data_slot(self, clicked):
        self.collect_file_info()
        self.data_load_ready_signal.emit(self.file)

    def collect_file_info(self):
        self.file.path = self.path_le.text()
        self.file.encoding = self.encoding_le.text()
        self.file.size = (self.size_le.text(), self.size_label.text())
        self.file.sep = self.csv_seperator_le.text()
        self.file.header_line = self.csv_header_le.text()
        self.file.sample_method = self.sample_method_cmbbox.currentText()
        self.file.sample_size = self.sample_size_le.text()

    # def show_path_warning(self, warning):
    #     if not warning:
    #         warning = ''
    #     self.path_warning_label.setText(warning)
    #
    # def handle_path(self, path,data_format):
    #     self.file.path = path
    #     record_num_estimation = self._estimate_record_num(data_format)
    #     if data_format in ('.csv', '.tsv'):
    #         self._handle_csv_path(data_format)
    #
    # def _handle_csv_path(self, data_format):
    #     self.csv_settings_widget.setEnabled(True)
    #     separator = ',' if data_format=='.csv' else '\t'
    #     self.csv_seperator_le.setText(separator)
    #
    # def _estimate_record_num(self,data_format):
    #     encoding = self.encoding_le.text().lower()
    #     if data_format in ('.csv', '.tsv'):
    #         approximate_record_number()
    #
    # def _detect_encoding(self):
    #     if self.path:
    #         if self.encoding_le.text().strip():
    #             self.encoding = self.encoding_le.text().strip()
    #         else:
    #             check_encoding(self.path)


