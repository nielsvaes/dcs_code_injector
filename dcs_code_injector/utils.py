import re

def check_regex(s):
    try:
        re.compile(s)
    except re.error:
        return False
    return True