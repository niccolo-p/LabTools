
from LabTools.utils.uncertainties import *

from uncertainties import ufloat

def test_unarray_unpackuarray():
    a = numpy.array([ufloat(2, 3), ufloat(4, 5), ufloat(6., 7.)])
    b = numpy.array([2, 4, 6.])
    c = numpy.array([3, 5, 7.])
    d = numpy.array([3.])
    
    b_, c_ = unpack_unarray(a)
    assert(b.all() == b_.all())
    assert(c.all() == c_.all())
    
    a_ = unarray(b, c)
    assert(str(a_.all()) == str(a.all())) # We need str beacuse uncertainties behavio
    
    assert(str(a.all()) == str(unarray(*unpack_unarray(a)).all()))
    b__, c__ = unpack_unarray(unarray(b, c))
    assert(b__.all() == b.all())
    assert(c__.all() == c.all())
    try:
        unarray(a, d)
    except IndexError:
        pass
