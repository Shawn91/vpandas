import os
import random

import chardet

from settings import generate_response

def check_is_file(file_path):
    """Check wheter the value of file_path argument is a valid file path"""
    if not os.path.isfile(file_path):
        return generate_response(result=False, warning='File not found. Please check the file path passed in.')
    return generate_response(result=True)

def check_encoding(file_path_or_text=None):
    if check_is_file(file_path_or_text)['result']:
        with open(file_path_or_text,'rb') as f:
            file_path_or_text = b''.join(f.readline() for _ in range(100))
    return generate_response(result=chardet.detect(file_path_or_text)['encoding'])

def check_file_size(file_path):
    if check_is_file(file_path)['result']:
        size = os.path.getsize(file_path)
        return generate_response(result=size)

def approximate_record_number(file_path, encoding=None):
    """Get an estimation of number of data records of a text file or a database
    Args:
        encoding: Encoding of the file. If set to falsy values, a Python library called `chardet` will be used to detect the encoding.
    
    Returns:
        int: Approximate number of lines in the file. 0 if the file is empty.
    """
    NUM_TEST_LINES = 1000
    is_file = check_is_file(file_path)
    if is_file['result']:
        raw_text = []
        with open(file_path, 'rb') as f: # read the first 1000 lines
            for _ in range(NUM_TEST_LINES):
                try:
                    raw_text.append(next(f))
                except StopIteration:
                    break
            NUM_TEST_LINES = len(raw_text)
            raw_text = b''.join(raw_text)
        if raw_text:
            if not encoding:
                encoding = chardet.detect(raw_text)['encoding']
            raw_text_size = len(raw_text.decode(encoding))
            file_size = check_file_size(file_path)['result']
            if raw_text_size:
                return generate_response(result=int(file_size / raw_text_size * NUM_TEST_LINES))
            else: # raw_text_size is zero
                return generate_response(warning='An error occured and the program faild to obtain an estimation of the line count.')
        else: # empty file
            return generate_response(result=0, warning='The file is empty')
    else: # not a file
        return is_file

def get_exact_record_num(file_path, encoding=None):
    """"""
    return

def sample_distinct_lines_from_file(path, total_num_lines=None, sample_size=100, skip_first_nlines=1, encoding='utf-8', random_seed=42):
    """Quickly sample distinct lines from a text file.
    If the sample_size is close to the line count of the file, the entire file will be read.

    If the file contains many duplicate lines, the returned sample may contain less lines than 
    specified by the sample_size parameter.

    The algorithm has an element of randomness, so if you are lucky (or unlucky) enough, 
    the returned sample may still contain less lines than specified by the sample_size parameter.

    For a detailed explanation of the algorithm, see the third algorithm on 
    http://metadatascience.com/2014/02/27/random-sampling-from-very-large-files/.

    Returns:
        list: List of lines sampled.
    """
    is_file = check_is_file(path)
    if is_file['result']:
        sample = {}
        file_size = os.path.getsize(path)
        if not total_num_lines:
            total_num_lines_res = approximate_record_number(path, encoding=encoding)
            if isinstance(total_num_lines_res['result'], int): # successfully estimated line count of the file
                total_num_lines = total_num_lines_res['result']
            else:
                return total_num_lines_res
        
        with open(path, 'rb') as f:
            if skip_first_nlines and isinstance(skip_first_nlines, int):
                first_nlines_to_skip = set(f.readline() for _ in range(skip_first_nlines))
            else:
                first_nlines_to_skip = set()
            # if sample size is almost the same as the line count, will simply read the whole file
            if total_num_lines / sample_size < 1.2: 
                lines = [line.decode(encoding) for line in f.readlines() if line not in first_nlines_to_skip]
                if len(lines) >= sample_size:
                    return generate_response(result=random.sample(lines, sample_size))
                else:
                    return generate_response(result=lines, warning='Sample size is larger than the line count, so the entire file is returned')
            else:
                random.seed(random_seed)
                sampling_times = 0
                while len(sample) < sample_size and sampling_times <= sample_size*2:
                    pos = random.randrange(file_size)
                    f.seek(pos)
                    f.readline() # skip a broken line
                    line = f.readline()
                    if line in first_nlines_to_skip:
                        continue
                    sample.setdefault(line, pos)
                    sampling_times += 1
                sample = sorted(sample.items(), key=lambda x:x[1])
                sample = [line.decode(encoding) for (line, pos) in sample][:sample_size]
                if len(sample) < sample_size:
                    warning = 'The program has sampled  %i times and still not been able to sample %i distinct lines.\nPossible reasons are 1. there are many duplicate lines in the file,\n2. there is a lurking bug in the code,\nor 3. you are just extremely unlucky.' % (sample_size*2, sample_size)
                    return generate_response(result=sample, warning=warning)
                return generate_response(result=sample)
        
    else:
        return is_file        

def parse_data_format_from_path(path):
    """Extract data format from path.
    Args:
        path(str): File path or database URI.
    Returns:
        str: Parsed data format
    """
    data_format = None
    if os.path.isfile(path):
        data_format = os.path.splitext(path)[1].lower()
    else:
        # TODO: Add support for more data formats
        pass

    if data_format is None:
        return generate_response(warning='The path %s is not understandable.' % path)
    # elif data_format not in supported_formats:
    #     return generate_response(warning='The data format %s is currently not supported.' % data_format)
    return generate_response(result=data_format)

def parse_json_format(file_path=None):
    """Detect whether a json file is a standard json or jsonl(json lines)
    Retures:
        str: json or jsonl
    """
    is_file_res = check_is_file(file_path)
    if is_file_res['result']:
        with open(file_path) as f:
            if f.readline().strip().startswith('['):
                return generate_response(result='jsonl')
            return generate_response(result='json')
    else:
        return is_file_res

if __name__ == "__main__":
    print(check_encoding(r'C:\Users\zyx199199\Desktop\a.txt',1,1))