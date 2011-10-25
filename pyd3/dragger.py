"""
Strips characters from a string file or path input created by
drag and drop a file or path into terminal shell.
"""

import os

def terminal(string):
    """
    Strips characters from a string file or path input created by
    drag and drop a file or path into terminal shell.
    
    - Unix/Linux/MacOS/BSD/etc -- remove backward slashes
    - DOS/Windows -- remove double quotes from the beginning and ending of string
    
    Arguments:
    :param string: string -- path of filename
    
    :return: string
    """
    if os.name is 'posix':
        if string[0] == "'" and string[-1] == "'": 
            #GNU/Linux (Ubuntu at least) treat the files that you can include with drag and drop, adding single quotes
            return string.replace("'", '')
        #OSX scape spaces with double backslash
        return string.replace('\\', '')
    
    if os.name in ('nt', 'dos', 'ce'):
        #Windows treat the files that you can include with drag and drop, adding double quotes
        return string.replace('"', '')
    
    return string