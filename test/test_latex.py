
from LabTools.latex import Variable, Decimal, UDecimal 

def test_variable():
    # Basic methods testing
    v = Variable("name", "value")
    assert(v.latexcode() == "\\newcommand{\\name}{value}")
    v.setname("n4m3")
    assert(v.latexcode() == "\\newcommand{\\n4m3}{value}")
    v.setvalue("v4lu3")
    assert(v.latexcode() == "\\newcommand{\\n4m3}{v4lu3}")
    
    # 

def test_udecimal():
    ud = UDecimal("R", 3423.34768, 8.2385)
    assert(ud.latexcode() == "\\newcommand{\\R}{3423.3 \\pm 8.2 e0}")
    ud.setuncdigit(3)
    assert(ud.latexcode() == "\\newcommand{\\R}{3423.35 \\pm 8.24 e0}")

    ud1 = UDecimal("test", 87, 7)
    try:
        assert(ud1.latexcode() == "\\newcommand{\\test}{87.0 \\pm 7.0 e0}")
    except Warning:
        pass
    ud1.setuncdigit(1)
    assert(ud1.latexcode() == "\\newcommand{\\test}{87 \\pm 7 e0}")
    ud1.setunc(7.0)
    assert(ud1.latexcode() == "\\newcommand{\\test}{87 \\pm 7 e0}")
    ud1.setuncdigit(4)
    try:
        assert(ud1.latexcode() == "\\newcommand{\\test}{87.000 \\pm 7.000 e0}")
    except Warning:
        pass
