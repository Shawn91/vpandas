import os

import pandas as pd
import math

import utilities

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

    def _load_csv(self, file_path, data_format, encoding='utf-8',nrows=10000, random_selection=False, **kwargs):
        """Loat a csv/tsv file into dataframe. If the file is too large for memory, nrows argument could be set to read only certain number of lines.
        Args:
            nrows(int): Total number of rows needed. Defaults to 10000 and if set to 0 or None or other falsy values, 
                the entire dataframe read from the path will be returned.
            random_selection(boolean): Select rows randomly if set to True, otherwise the first nrows will be returned.
        """
        if 'sep' not in kwargs:
            kwargs['sep'] = '\t' if data_format == '.tsv' else ','
        
        if not nrows:
            return pd.read_csv(filepath_or_buffer=file_path, **kwargs)

        total_num_lines = utilities.approximate_line_count(file_path, encoding=encoding)
        if total_num_lines / self.CHUNK_SIZE < 1.1:
            return pd.read_csv(filepath_or_buffer=file_path, **kwargs)

        elif not random_selection:
            return pd.read_csv(filepath_or_buffer=file_path, nrows=nrows,**kwargs)

        else:
            num_chunks = math.ceil(total_num_lines / self.CHUNK_SIZE)
            num_lines_per_chunk = math.ceil(nrows / num_chunks)
            pd_reader = pd.read_csv(filepath_or_buffer=file_path, **kwargs, chunksize=self.CHUNK_SIZE)
            result_df = pd.DataFrame()
            for chunk in pd_reader: # read 300 thousand lines a time
                 result_df = result_df.append(self._select_rows(chunk, nrows=num_lines_per_chunk, random_selection=random_selection), ignore_index=True)
                 if result_df.shape[0] >= nrows:
                     return result_df.iloc[0:nrows]

    def load_data(self, file_path=None, data_format=None, nrows=10000, random_selection=False,**kwargs):
        if not isinstance(file_path, str):
            raise TypeError('path is supposed to be a string but received %s of type %s' % (str(file_path), type(file_path)))
        data_format = self._parse_data_format(file_path, data_format)
        
        if data_format in ('.csv', '.tsv'):
            return self._load_csv(file_path=file_path, data_format=data_format,nrows=nrows, random_selection=random_selection, **kwargs)

pandas_loader = PandasLoader()

if __name__ == "__main__":
    print(pandas_loader.load_data(r'E:\Study\microsoft-malware-prediction\train.csv',nrows=1000, random_selection=True))