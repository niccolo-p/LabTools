
#  LabTools - generic.py
#  Copyright 2019 Luca Arnaboldi

import inspect
from uncertainties import unumpy as unp

def sprint(obj):
    """
    Super Print. Print a variable with its name.
    """
    def retrieve_name(var):
        """
        Copy-pasted from StackOverflow
        """
        callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
        return [var_name for var_name, var_val in callers_local_vars if var_val is var]
    
    obj_name = retrieve_name(obj)[0]
    
    print("{0}: {1}".format(obj_name, obj))

def decibel(x):
    """
    Convert a value in decibel.
    """
    return 20. * unp.log10(x)
