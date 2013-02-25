from datetime import datetime

def num(x):
    if x:
        try:
            return float(x) if '.' in x else int(x)
        except ValueError:
            return 0
    return 0

def uuid():
    return datetime.now().strftime('%y%m%d%H%M%S%f')

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

import traceback
def trace_back():  
    try:  
        return traceback.format_exc()  
    except:  
        return ''
