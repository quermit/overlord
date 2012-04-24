"""
Created on Apr 24, 2012

@author: quermit
"""

def total_seconds(td):
    """The function that is missing in datetime.timedelta in python 2.6."""
    try:
        return td.total_seconds()
    except AttributeError:
        # formula found at http://docs.python.org/library/datetime.html
        return (td.microseconds + (
                td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10.0 ** 6
