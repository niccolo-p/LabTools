
#  LabTools - latex.py
#  Copyright 2019 Luca Arnaboldi

import numpy
import math
import uncertainties as unc
from uncertainties import unumpy

def unarray(data, u_data):
    """
    Crea a numpy.array of ufloat given two arrays of float.
    
    This function is now deprecated since it's already implemented in unumpy.
    This is now only a redirect to unumpy mantained for retrocompability.
    """
    
    if len(data) != len(u_data):
        raise IndexError('Two arrays have different leght: {0} and {1}'.format(
        len(data),
        len(u_data),
    ))
    
    # Old Version
    # return numpy.array([unc.ufloat(data[i], u_data[i]) for i in range(0, len(data))])

    return unumpy.uarray(data, u_data)
    

def unpack_unarray( u_array ):
    """
    Divide an array of ufloats in two numpy.array of floats.
    It works also for unumpy.uarray and tuple.
    """
    data = numpy.zeros(len(u_array))
    u_data = numpy.zeros(len(u_array))
    
    for i in range(0, len(u_array)):
        data[i] = u_array[i].n
        u_data[i] = u_array[i].s
        
    return data, u_data
    
    
def de2unc(value, dig, percent = 0., quad = True):
    # Double Error to uncertainties
    """
    Given a value with its digit error and percentage error return the uncertaties
    element.
    If quad is true the error are summated in quadrature.
    """
    err_perc = value * percent / 100
    if quad:
        error = numpy.sqrt(dig**2 + err_perc**2)
    else:
        error = dig + err_perc
    
    # Try with floats
    try:
        return unc.ufloat(value, error)
    # Use arrays
    except AttributeError:
        return unarray(value, error)
        
        

    
