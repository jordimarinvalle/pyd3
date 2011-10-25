"""
Screen Cleaner :: screaner

Clean OS terminal screen on:
    - Unix/Linux/MacOS/BSD/etc
    - DOS/Windows
    - Anything Else ;)
"""

import os

def screaner():
    """
    Clean OS terminal screen on:
        - Unix/Linux/MacOS/BSD/etc
        - DOS/Windows
        - Anything Else ;)
    """
    if os.name is 'posix':
        return os.system('clear')
    
    if os.name in ('nt', 'dos', 'ce'):   
        return os.system('cls')
    
    print '\n'*100
    