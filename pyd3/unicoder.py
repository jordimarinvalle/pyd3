"""
Converts a byte string into a unicode string, 
ready to be printed into console terminal.
"""

def unicoder(string):
    """
    Converts a byte string into a unicode string, 
    ready to be printed into console terminal.
    
    Arguments:
    :param string: string -- string of characters
    
    :return: unicode string
    """
    try: string = unicode(str(string))
    except (UnicodeDecodeError, UnicodeEncodeError): pass
    return string