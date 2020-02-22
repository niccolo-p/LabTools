
from LabTools.measure import *


def test_instrument():
    i = Instrument('test/inputs/instrument1.yaml')
    assert(str(i.measure('tipo1', 15.)) == '15+/-10')
    assert(str(i.measure('tipo1', 74.6)) == '75+/-12')
    assert(str(i.measure('tipo1', 0.34)) == '0.34+/-0.05')
    
    assert(str(i.measure('tipo2', 1.876)) == '1.876+/-0.031')
    assert(str(i.measure('tipo2', 1.876, 5.000)) == '1.876+/-0.021')
    
    # Tipo che non esiste
    try:
        i.measure('tipononesiste', 0.)
    except KeyError:
        pass
        
    # Provo a passare un value che non è un float
    try:
        i.measure('tipo1', 'uno')
    except ValueError:
        pass
        
    # Fuori il fondoscala più grande
    try:
        i.measure('tipo1', 5000.)
    except ValueError:
        pass
        
    # Fondoscala che non esiste
    try:
        i.measure('tipo1', 5., fond = 50.)
    except ValueError:
        pass
        
def test_tester():
    pass
    # Io spero funzionino
    
    
