
from LabTools.utils import significant_digits as sd
from LabTools.utils import move_decimal as md
from LabTools.utils import most_significant_digit as msd
from LabTools.utils import pair_decimal_with_uncertainty as pdwu

def test_most_significant_digit():
    assert(msd(0.34) == -1)
    assert(msd(1234) == 3)
    assert(msd(-0.64) == -1)

def test_significant_digits():
    assert(sd(0.000345, 2) == ("3.4", -4))
    assert(sd(-0.000345, 2) == ("-3.4", -4))
    assert(sd(0.000345, 5) == ("3.4500", -4))
    assert(sd(0., 5) == ("0.0000", 0))

    assert(sd(9873.657, 3) == ("9.87", 3))
    assert(sd(9873.657, 4) == ("9874", 0))
    assert(sd(9873.657, 14) == ("9873.6570000000", 0))

    ## Compact True
    assert(sd(0.000345, 2, True) == "3.4e-4")
    assert(sd(0.000345, 5, True) == "3.4500e-4")
    assert(sd(0., 5, True) == "0.0000")

    assert(sd(9873.657, 3, True) == "9.87e+3")
    assert(sd(9873.657, 4, True) == "9874")
    assert(sd(9873.657, 14, True) == "9873.6570000000")
    assert(sd(987365778672678, 2, True) == "9.9e+14")
    
def test_move_decimal():
    assert(md("34.35", 5) == "3435000")
    assert(md("34.35", 2) == "3435")
    assert(md("34.35", 1) == "343.5")
    assert(md("34.35", 0) == "34.35")
    assert(md("34.35", -1) == "3.435")
    assert(md("34.35", -2) == "0.3435")
    assert(md("34.35", -5) == "0.0003435")

def test_pair_decimal_with_uncertainty():
    # Weak!
    # I think the function is properly tested anyway by test_udecimal in test_latex.py
    assert(pdwu(345.678, 1.234, 2) == ('345.7', '1.2', 0, False))
    pass
