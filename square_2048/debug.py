#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 17:44:06 2020

@author: pi
"""

import time
from functools import wraps

def timethis(func):
    '''
    Decorator that reports time spent.
    from - Python Cookbook 3rd Ed.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result=func(*args, **kwargs)
        end = time.time()
        print(func.__qualname__,end-start)
        return result
    return wrapper
