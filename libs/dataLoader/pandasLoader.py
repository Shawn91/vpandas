import os

import pandas as pd

class PandasLoader:
    """load data into pandas dataframe

    Args:
        path(str): File path or database URI
        data_format(str, optional): Explicitly telling what the file type is. Defaults to None.
            Possible values include `csv`,`tsv`,`json`,`mongob`,`sql`, etc
    
    Attributes:
        supported_data_format(list): Currently supported data format.

    Todo:
        Add support for more data formats. Currently, only csv files are supported.
    """

    supported_data_format = ('csv','tsv')

    def __init__(self):
        pass

    def _parse_data_format(self, path, data_format):
        if data_format is None:
            if os.path.isfile(path):
                data_format = os.path.splitext(path)[1]
            else:
                # TODO: Add support for more data formats
                pass
        elif not isinstance(data_format, str):
            raise TypeError('data_format is supposed to be a string but received %s of type %s' % (str(data_format), type(data_format)))
        
        if data_format not in self.supported_data_format:
            raise ValueError('data_format received unsupported data format %s' % str(data_format))
        return data_format
    
    def _load_csv(self, path, data_format, **kwargs):
        if 'sep' not in kwargs:
            kwargs['sep'] = '\t' if data_format == 'tsv' else ','
        return pd.read_csv(filepath_or_buffer=path, **kwargs)
    
    def load_data(self, path=None, data_format=None, **kwargs):
        if not isinstance(path, str):
            raise TypeError('path is supposed to be a string but received %s of type %s' % (str(path), type(path)))
        data_format = self._parse_data_format(path, data_format)
        
        if data_format in ('csv', 'tsv'):
            return self._load_csv(**kwargs)

pandas_loader = PandasLoader()