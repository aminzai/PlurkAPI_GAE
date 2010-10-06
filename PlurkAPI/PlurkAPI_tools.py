# -*- coding: utf8 -*-

import datetime

def datetime_from_plurk_string(s):
    return datetime.datetime(2000,1,1).strptime(s, '%a, %d %b %Y %H:%M:%S %Z')

def conv_datetime(v):
    return v.isoformat()

def getDatetime(self , x ):
    return x.isoformat()

def getToday():
    return datetime.date.today()

def ctlDay( date , num ):
    """
    if type( date ) == 'datetime':
        return date.replace( day = date.day + num )
    else:
        return None
    """
    return date.replace( day = date.day + num )
