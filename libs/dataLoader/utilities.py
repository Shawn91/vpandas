import os
import chardet

def is_file(file_path, raise_exception=False):
    """Check wheter the value of file_path argument is a valid file path"""
    if not os.path.isfile(file_path):
        if raise_exception:
            raise FileNotFoundError('File not found. Please check the file path passed in')
        return False
    return True

def approximate_line_count(file_path, encoding='utf-8', raise_exception=False):
    """Get an estimation of number of lines of a text file
    Args:
        encoding: Encoding of the file. Defaults to utf-8. If set to falsy values, a Python library called `chardet` will be used to detect the encoding.
    
    Returns:
        int: Approximate number of lines in the file. 0 if the file is empty and -1 if some error occures and raise_exception set to False.
    """
    NUM_TEST_LINES = 1000
    if is_file(file_path, raise_exception=raise_exception):
        with open(file_path, 'rb') as f: # read the first 1000 lines
            try:
                raw_text = b''.join(next(f) for _ in range(NUM_TEST_LINES))
            except StopIteration:
                pass
        
        if raw_text:
            if not encoding:
                encoding = chardet.detect(raw_text)['encoding']

            raw_text_size = len(raw_text.decode(encoding))
            file_size = os.path.getsize(file_path)
            if raw_text_size:
                return int(file_size / raw_text_size * NUM_TEST_LINES)
            elif raise_exception:
                raise Exception('Some error occured and the estimation of line count cannot be obtained.')
            else: # raw_text_size is zero
                return -1
        else: # empty file
            return 0
    else: # not a file and raise_exception set to False
        return -1



if __name__ == "__main__":
    print(approximate_line_count(r'C:\Users\zyx199199\Desktop\a.txt',encoding=None))