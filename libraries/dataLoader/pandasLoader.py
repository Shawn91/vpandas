import os
import math
import io

import pandas as pd
import chardet

from settings import generate_response
from libraries.dataLoader import utilities

class PandasLoader:
    """load data into pandas dataframe

    Args:
        path(str): File path or database URI
        data_format(str, optional): Explicitly telling what the file type is. Defaults to None.
            Possible values include `csv`,`tsv`,`json`,`mongob`,`sql`, etc
    
    Attributes:
        SUPPORTED_DATA_FORMAT(list): Currently supported data format.

    Todo:
        Add support for more data formats. Only csv files are currently supported.
    """

    SUPPORTED_DATA_FORMAT = ('.csv','.tsv')
    CHUNK_SIZE = 300000


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
        
        if data_format not in self.SUPPORTED_DATA_FORMAT:
            raise ValueError('data_format received unsupported data format %s' % str(data_format))
        return data_format
    
    @staticmethod
    def _select_rows(df, nrows=1, random_selection=False):
        """Select certain number of rows from a dataframe
        Args:
            nrows(int): Number of rows needed. Defaults to 1 and if set to 0 or None the entire dataframe will be returned
            random_selection(boolean): Select rows randomly if set to True, otherwise the first nrows will be returned 
        """
        if nrows:
            if random_selection:
                return df.sample(n=nrows, random_state=42) # not truly random to ensure the same dataframe will ge generated
            else:
                return df.head(nrows)
        else:
            return df

    def _load_csv(self, file_path, data_format, encoding=None, nrows=None, selection_method='random', **kwargs):
        """Loat a csv/tsv file into dataframe. If the file is too large for memory, nrows argument could be set to read only certain number of lines.
        Args:
            header_line: Indicate whether first line is header. Legitimate values are 0, True, False. 0 and True mean the first 
                line is header and False means otherwise. Hierarchical index is not currently supported.
            nrows(int): Select certain number of rows to return. Defaults to None and if set to 0 or None or other falsy values, 
                the entire dataframe read from the path will be returned in regardless of the size of the file.
            selection_method(str): Select rows randomly if set to 'random'. Legitimate values are 'random', 'first'.
        """
        if selection_method and selection_method.lower() not in ('random', 'first'):
            return generate_response(warning='Received invalid value %s for parameter selection_method'%str(selection_method))

        if 'sep' not in kwargs:
            kwargs['sep'] = '\t' if data_format == '.tsv' else ','
        
        if not nrows: # return the entire dataframe in regardless of the size of the file
            return generate_response(result=pd.read_csv(filepath_or_buffer=file_path,encoding=encoding,**kwargs))

        total_num_lines_res = utilities.approximate_line_count(file_path, encoding=encoding)
        if not total_num_lines_res['result']:
            return total_num_lines_res
        
        if total_num_lines_res['result'] / self.CHUNK_SIZE < 1.2:
            return generate_response(result=pd.read_csv(filepath_or_buffer=file_path, encoding=encoding,**kwargs))

        elif selection_method == 'first':
            return generate_response(result=pd.read_csv(filepath_or_buffer=file_path, nrows=nrows,encoding=encoding,**kwargs))

        else: # randomly select nrows
            skip_first_nlines = 0 # number of rows at the beginning to skip
            header = None # header line
            if 'skiprows' in kwargs:
                skip_first_nlines += int(kwargs['skiprows'])
                del kwargs['skiprows']
            if 'header' in kwargs:
                if (kwargs['header'] == 0 or kwargs['header'] == 'infer'):
                    with open(file_path, encoding=encoding) as f:
                        header = f.readline()
                    skip_first_nlines += 1
            sampled_lines_res = utilities.sample_distinct_lines_from_file(file_path=file_path, total_num_lines=total_num_lines_res['result'], sample_size=nrows, skip_first_nlines=skip_first_nlines,encoding=encoding)
            sampled_lines = sampled_lines_res['result']
            sampled_lines_warning = sampled_lines_res['warning']
            if sampled_lines:
                warning = '' if len(sampled_lines_res) == nrows else sampled_lines_warning
                if header:
                    sampled_lines.insert(0, header)
                sampled_lines_df = pd.read_csv(io.StringIO(''.join(sampled_lines)), **kwargs)
                return generate_response(result=sampled_lines_df, warning=warning)
            else:
                return sampled_lines_res

    def load_data(self, file_path=None, data_format=None, encoding=None, nrows=10000, random_selection=False,**kwargs):
        if not isinstance(file_path, str):
            raise TypeError('path is supposed to be a string but received %s of type %s' % (str(file_path), type(file_path)))
        data_format = self._parse_data_format(file_path, data_format)
        
        if data_format in ('.csv', '.tsv'):
            selection_method = 'random' if random_selection else 'first'
            if not encoding:
                encoding = utilities.check_encoding(file_path)['result']
            return self._load_csv(file_path=file_path, data_format=data_format, encoding=encoding, nrows=nrows, selection_method=selection_method, **kwargs)

pandas_loader = PandasLoader()

if __name__ == "__main__":
    with open(r'E:\Study\projects\Wiki_Cities\2.csv') as f:
        encoding = chardet.detect(f.read())['encoding']
        print(encoding)
    print(pandas_loader.load_data(r'E:\Study\projects\Wiki_Cities\2.csv',nrows=10, encoding=encoding,random_selection=True, skiprows=1,header=None))