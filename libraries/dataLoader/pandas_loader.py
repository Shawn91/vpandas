import os
import math
import io

import pandas as pd
import chardet

import settings
from settings import generate_response
from libraries.dataLoader import utilities

class PandasLoader:
    """load data into pandas dataframe

    Args:
        path(str): File path or database URI
        data_format(str, optional): Explicitly telling what the file type is. Defaults to None.
            Possible values include `csv`,`tsv`,`json`,`mongob`,`sql`, etc

    Attributes:
        SAMPLE_SIZE(int): Default number of data records for sampling.

    Todo:
        Add support for more data formats. Only csv files are currently supported.
    """

    SAMPLE_SIZE = 30000

    def _load_csv(self, path, encoding=None, sample_size=None, sample_method='random', sep=',', header_line=0,record_num=None,**kwargs):
        """Loat a csv/tsv file into dataframe. If the file is too large for memory, sample_size argument could be set to read only certain number of lines.
        Args:
            header_line: Indicate whether first line is header. Legitimate values are 0, True, False. 0 and True mean the first 
                line is header and False means otherwise. Hierarchical index is not currently supported.
            sample_size(int): Select certain number of rows to return. Defaults to None and if set to 0 or None or other falsy values, 
                the entire dataframe read from the path will be returned in regardless of the size of the file.
            sample_method(str): Select rows randomly if set to 'random'. Legitimate values are 'random', 'first'.
        """
        if sample_method and sample_method.lower() not in ('random', 'first', 'all'):
            return generate_response(warning='Received invalid value %s for parameter sample_method'%str(sample_method))

        if not sample_size or (sample_method and sample_method=='all'): # return the entire dataframe in regardless of the size of the file
            return generate_response(result=pd.read_csv(filepath_or_buffer=path,encoding=encoding,sep=sep,header=header_line,**kwargs))

        elif sample_method == 'first':
            return generate_response(result=pd.read_csv(filepath_or_buffer=path, nrows=int(sample_size),encoding=encoding,sep=sep, **kwargs))

        else: # randomly select sample_size
            skip_first_nlines = 0 # number of rows at the beginning to skip
            header = None # header line
            if 'skiprows' in kwargs:
                skip_first_nlines += int(kwargs['skiprows'])
                del kwargs['skiprows']
            if header_line == 0 or header_line == 'infer':
                with open(path, encoding=encoding) as f:
                    header = f.readline()
                skip_first_nlines += 1
            sampled_lines_res = utilities.sample_distinct_lines_from_file(path=path, total_num_lines=record_num, sample_size=sample_size, skip_first_nlines=skip_first_nlines,encoding=encoding)
            sampled_lines = sampled_lines_res['result']
            sampled_lines_warning = sampled_lines_res['warning']
            if sampled_lines:
                warning = '' if len(sampled_lines_res) == sample_size else sampled_lines_warning
                if header:
                    sampled_lines.insert(0, header)
                sampled_lines_df = pd.read_csv(io.StringIO(''.join(sampled_lines)),sep=sep,  **kwargs)
                return generate_response(result=sampled_lines_df, warning=warning)
            else:
                return sampled_lines_res

    def load_data(self, path=None, data_format=None, encoding=None, sample_size=None, sample_method=None, sep=None, header_line=None, record_num=None, **kwargs):
        if data_format:
            if data_format in ('.csv', '.tsv'):
                return self._load_csv(path=path, encoding=encoding, sample_size=sample_size,sample_method=sample_method,
                                      sep=sep, header_line=header_line,record_num=record_num,**kwargs)

pandas_loader = PandasLoader()

if __name__ == "__main__":
    # print(pandas_loader.load_data(r'E:\Study\projects\Wiki_Cities\2.csv',sample_size=10, encoding=encoding,random_selection=True, skiprows=1,header=None))
    print(pandas_loader.load_data({'path': 'E:/Study/microsoft-malware-prediction/sample_submission.csv', 'encoding': 'ascii', 'size': '277', 'size_unit': 'MB', 'data_format': '.csv', 'record_num': {'exact': None, 'estimated': 7854315}, 'sample_size': '1000', 'sample_method': 'first', 'separator': ',', 'headers': [], 'header_line': '1'} ))