
from LabTools.utils.generic import *
from uncertainties import ufloat, unumpy


def test_sprint(capfd):
    a = 'marco'
    b = 45.
    c = [12, 45]
    d = ufloat(b,b)
    e = unumpy.uarray(c, c)
    
    sprint(a)
    out, err = capfd.readouterr()
    assert(out == 'a: marco\n')
    
    sprint(b)
    out, err = capfd.readouterr()
    assert(out == 'b: 45.0\n')
    
    sprint(c)
    out, err = capfd.readouterr()
    assert(out == 'c: [12, 45]\n')
    
    sprint(d)
    out, err = capfd.readouterr()
    assert(out == 'd: (4+/-4)e+01\n')
    
    sprint(e)
    out, err = capfd.readouterr()
    assert(out == 'e: [12.0+/-12.0 45.0+/-45.0]\n')
