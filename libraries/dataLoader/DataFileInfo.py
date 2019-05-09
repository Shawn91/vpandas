"""Contains info of the file/database loaded
Todo:
    Finish the get_exact_record_num function.
"""

from libraries.dataLoader import utilities
import settings

class DataFileInfo:
    __slots__ = (
        '_path',
        '_data_format',
        '_encoding',
        '_size',
        '_estimated_record_num',
        '_exact_record_num',
        '_separator',
        '_headers',
        '_header_line',
        'warnings'
    )
    def __init__(self, file_path=None):
        self._path = file_path
        self._encoding = None
        self._data_format = None
        self._size = ('', '') # first element for number of size, second element for unit
        self._estimated_record_num = None
        self._exact_record_num = None
        self._separator = ''
        self._headers = []
        self._header_line = 1
        self.warnings = {}

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, new_path):
        is_file_res = utilities.check_is_file(new_path)
        if is_file_res['result']:
            self._path = new_path
            self.infer_from_path()
        else:
            self.warnings['path'] = is_file_res['warning']

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, new_size):
        self._size = new_size

    @property
    def data_format(self):
        return self._data_format
    @data_format.setter
    def data_format(self, new_data_format):
        if new_data_format in settings.SUPPORTED_DATA_FORMAT:
            self._data_format = new_data_format
        else:
            self._data_format = ''
            self.warnings['path'] = 'The data format %s is currently not supported.' % new_data_format

    @property
    def encoding(self):
        return self._encoding
    @encoding.setter
    def encoding(self, new_encoding):
        self._encoding = new_encoding

    @property
    def estimated_record_num(self):
        return self._estimated_record_num
    @estimated_record_num.setter
    def estimated_record_num(self, new_estimated_record_num):
        self._estimated_record_num = new_estimated_record_num

    @property
    def exact_record_num(self):
        return self._exact_record_num
    @exact_record_num.setter
    def exact_record_num(self, new_exact_record_num):
        self._exact_record_num = new_exact_record_num

    @property
    def separator(self):
        return self._separator
    @separator.setter
    def separator(self, new_separator):
        self._separator = new_separator

    @property
    def headers(self):
        return self._headers
    @headers.setter
    def headers(self, new_headers):
        self._headers = new_headers

    @property
    def header_line(self):
        return self._header_line
    @header_line.setter
    def header_line(self, new_header_line):
        self._header_line = new_header_line

    def get_all_properties(self):
        return {'path':self.path, 'encoding':self.encoding, 'size':self.size[0], 'size_unit':self.size[1],'data_format':self.data_format,
                'record_num':{'exact':self.exact_record_num, 'estimated':self.estimated_record_num},
                'separator':self.separator, 'headers':self.headers, 'header_line':self.header_line}

    def delete_warning(self, warning_field):
        if warning_field in self.warnings:
            del self.warnings[warning_field]

    def infer_from_path(self, new_encoding=None):
        if new_encoding is None:
            new_encoding = utilities.check_encoding(self.path)['result']
        self.encoding = new_encoding

        self.size = settings.convert_bytes(utilities.check_file_size(self.path)['result'])

        data_format_res = utilities.parse_data_format_from_path(self.path)
        if data_format_res['result']:
            self.data_format = data_format_res['result']
        else:
            self.data_format = ''
            self.warnings['path'] = data_format_res['warning']

        if self.data_format:
            if self.data_format in ('.csv', '.tsv'):
                self.separator = ',' if self.data_format == '.csv' else '\t'
        else:
            self.separator = ''

        est_record_num_res = utilities.approximate_record_number(self.path, self.encoding)
        if est_record_num_res['result'] or est_record_num_res['result'] == 0:
            self.estimated_record_num = est_record_num_res['result']
        else:
            self.warnings['estimated_record_num'] = est_record_num_res['warning']

        exc_record_num_res = utilities.get_exact_record_num(self.path, self.encoding)









if __name__ == '__main__':
    f = DataFileInfo('a')
    f.path = 'ha'
    print(vars(f))