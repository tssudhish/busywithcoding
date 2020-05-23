#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 17:44:06 2020

@author: pi
"""

import time
from functools import wraps, partial
import logging



def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func



def logged(level, name=None, message=None):
    '''
    Add loging to a function. 
    level is the logging level,
    name is the logger name, 
    message is the log message.
    
    If name and message are not specified they
    default to the functions's module and name.
    '''
    
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
    
        # attach setter functions
        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg
        
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel
    
        return wrapper
    return decorate



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
        print("For function {}, time taken {}".format(func.__qualname__,end-start))
        return result
    return wrapper
