import csv
import os
from .measurements.engagement import compute_engagement

def to_list(x):
    """ make a list out of x if it is not already a list"""
    if isinstance(x, list):
        return x
    try:
        return list(x)
    except TypeError:
        return [x]
    