
#  LabTools - fit.py
#  Copyright 2019 Luca Arnaboldi

from .utils import ucurve_fit, unpack_unarray
import uncertainties as unc
from uncertainties import unumpy
from scipy.misc import derivative
import numpy
from scipy.optimize import curve_fit

from functools import wraps

DEFAULT_CONVERGENCE_CONDITION = 1e-7
DEFAULT_MAX_ITERATION = 20


def chi2(f, param, X, Y):
    """
    Calculate the chi squared and the degree of freedom of a standard fit.
    X, Y must be uarrays!
    """
    @wraps(f)
    def model(x, *pars):
        return unumpy.nominal_values(f(x, *pars))
    x, ux = unpack_unarray(X)
    y, uy = unpack_unarray(Y)
    return sum(((y - model(x, *param)) / uy)**2), len(X) - len(param)
           
def iterated_fit(
    f,
    X,
    Y,
    p0 = None,
    df = None,
    absolute_sigma = False,
    convergence_condition = DEFAULT_CONVERGENCE_CONDITION,
    max_iterations = DEFAULT_MAX_ITERATION,
    ):
    """
    Iterated fit that propagates the errors on the X on the Y to account the x-axis
    error.
    If p0 is None is calculated with ucurve_fit without X error.
    If df is None it is used the numeric derivative from scipy. Not always work.
    """
    
    if df is None:
        raise NotImplementedError("Numeric derivatived not implemented yet!")
    else:
        @wraps(df)
        def dmodel(x, *pars):
            return unumpy.nominal_values(df(x, *pars))
    
    @wraps(f)
    def model(x, *pars):
        return unumpy.nominal_values(f(x, *pars))
    
    x, ux = unpack_unarray(X)
    y, uy = unpack_unarray(Y)
    
    # Now we can work with normal numpy functions, without unceraties
    
    par, cov = curve_fit(model, x, y, sigma = uy, p0 = p0, absolute_sigma = absolute_sigma)
    
    while --max_iterations:
        dif_y = numpy.sqrt(uy**2 + (dmodel(x, *par) * ux)**2)
        
        npar, ncov = curve_fit(
            model,
            x,
            y,
            sigma = dif_y,
            p0 = par,
            absolute_sigma = absolute_sigma
        )
        
        perror = numpy.abs(npar - par) / npar
        cerror = numpy.abs(ncov - cov) / ncov
        
        if (perror < convergence_condition).all() and (cerror < convergence_condition).all():
            break

        par = npar
        cov = ncov
        
    if max_iterations == 0:
        raise Warning("iterated_fit termined because max_iterations was reached.")
        
    return unc.correlated_values(par, cov)
    
def chi2iterated(f, param, X, Y, df = None):
    """
    Calculate the chi squared and degree of freedom taking to account the error
    on x axis.
    """
    if df is None:
        raise NotImplementedError("Numeric derivatived not implemented yet!")
    else:
        @wraps(df)
        def dmodel(x, *pars):
            return unumpy.nominal_values(df(x, *pars))
    @wraps(f)
    def model(x, *pars):
        return unumpy.nominal_values(f(x, *pars))
    
    x, ux = unpack_unarray(X)
    y, uy = unpack_unarray(Y)
    dif_y = numpy.sqrt(uy**2 + (ux * dmodel(x, *param))**2) # errore
    return sum(((y - model(x, *param)) / dif_y)**2), len(X) - len(param)
    
    
