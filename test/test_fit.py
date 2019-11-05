
from LabTools.fit import *

from LabTools.utils import unarray
import numpy
from uncertainties import unumpy, ufloat

# Import the testing of ucurve_fit from uncertainties tests.
from test_uncertainties import test_ucurve_fit as test_ucurve_fit_

"""
This is not testing the correcteness of the fit or the error propagation of
uncertainties. It is only checking if it works in every case I need.
"""
def model(x, a, b):
    return numpy.sqrt(a * x + b)
        
def umodel(x, a, b):
    return unumpy.sqrt(a * x + b)
        
def dumodel(x, a, b):
    return a / (2 * unumpy.sqrt(a * x + b))

x = numpy.array([3., 41., 100.])
y = numpy.array([5., 15., 25.])
ux = x / 100.
uy = y / 100.

X = unarray(x, ux)
Y = unarray(y, uy)

p0 = ucurve_fit(umodel, X, Y)

def test_ucurve_fit_with_chi2():
    print(chi2(umodel, p0, X, Y))

def test_iteraed_fit_with_chi2():
    p = iterated_fit(umodel, X, Y, df = dumodel)
    assert((p[0]-p0[0]).n < 0.01)
    assert((p[1] - p0[1]).n < 0.01)
    print(chi2iterated(umodel, p, X, Y, df = dumodel))
    
    # Not Coverge
    try:
        p = iterated_fit(umodel, X, Y, df = dumodel, max_iterations = 0)
    except Warning:
        pass
        
    # Numeric derivative
    try:
        p = iterated_fit(umodel, X, Y)
    except NotImplementedError:
        pass
    try:
        chi2iterated(umodel, p, X, Y)
    except NotImplementedError:
        pass
    
    
def test_ucurve_fit():
    test_ucurve_fit_()
    
