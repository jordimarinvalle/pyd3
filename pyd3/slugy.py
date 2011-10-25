"""
Replace non_ASCII characters with similar ASCII characters characters,
generating a new scring with only ASCII characters.

Weird characters with encoding problems, will be removed.
"""

import string
import unicodedata

def get_valid_chars():
    """Get valid characters.
    Valid characters are the ones which are on the following list:
    -_()[] abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
    
    Return: string
    """
    return "-_()[] %s%s" % (string.ascii_letters, string.digits)

def get_unicode_nde_str(string_of_chars):
    """
    Get a unicode normalized string (NFKD).
    Also the string is decoded (UTF8) and encoded (ASCII).
    
    Arguments:
    :param str: string
    
    Return: unicode string
    """
    return unicodedata.normalize('NFKD', string_of_chars.decode('UTF-8', 'ignore')).encode('ASCII', 'ignore')

def slugy(string_of_chars, separator = '_', lower=True):
    """
    Transform a string to a slugy string.
    
    Slugy string will only can contain ascii character and few more valid characters 
        -- such as middle dash, underscore, round brackets, space.
    Characters which don't complain conditions will be removed.
    
    In case that separator param is set, words are splitted by it.
    In case that lower param is not set, string will be returned on lowercase mode.
    
    Arguments:
    :param chars: string
    :param separator: string -- (a single char fits best). '_' char as default value.
    :param lower: boolean -- True as default value.
    """
    slugy_string = ""
    try:
        u_chars = ""
        valid_chars = get_valid_chars()
        string_of_chars = str(string_of_chars) #We can't assume that it will be a string ;)
        u_chars = get_unicode_nde_str(string_of_chars)
    except UnicodeEncodeError:
        for char in string_of_chars:
            try: u_chars += get_unicode_nde_str(char)
            except: pass
    string_of_chars = string.replace(str(u_chars), " ", separator)
    slugy_string = ''.join(char for char in string_of_chars if char in valid_chars).strip()
    return slugy_string.lower() if lower else slugy_string
