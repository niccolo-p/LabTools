
from LabTools.latex import Variable, Decimal, UDecimal, Document

from uncertainties import ufloat

def test_variable():
    # Basic methods testing
    v = Variable("name", "value")
    assert(v.latexcode() == "\\newcommand{\\name}{value}")
    v.setname("n4m3")
    assert(v.latexcode() == "\\newcommand{\\n4m3}{value}")
    v.setvalue("v4lu3")
    assert(v.latexcode() == "\\newcommand{\\n4m3}{v4lu3}")
    
    # 

def test_udecimal_starndard():
    ud = UDecimal("R", 3423.34768, unc = 8.2385)
    assert(ud.latexcode() == "\\newcommand{\\R}{3423.3 \\pm 8.2 e0}")
    ud.setuncdigit(3)
    assert(ud.latexcode() == "\\newcommand{\\R}{3423.35 \\pm 8.24 e0}")
    ud.setvalue(8.436)
    ud.setuncdigit(2)
    ud.setunc(0.056)
    assert(ud.latexcode() == "\\newcommand{\\R}{8.436 \\pm 0.056 e0}")

    ud1 = UDecimal("test", 87, unc = 7)
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
        
def test_udecimal_uncertainties():
    ud = UDecimal("test", ufloat(3423.34768, 8.2385))
    assert(ud.latexcode() == "\\newcommand{\\test}{3423.3 \\pm 8.2 e0}")
    
    a = ufloat(3.456, 0.056)
    b = ufloat(4.98, 0.000003)
    print(a + b)
    ud.setvalue(a + b)
    assert(ud.latexcode() == "\\newcommand{\\test}{8.436 \\pm 0.056 e0}")
    ud.setvalue(a*b)
    assert(ud.latexcode() == "\\newcommand{\\test}{17.21 \\pm 0.28 e0}")
    
    
    

def check_file_with_document(d, filename):
    with open(filename) as f:
        cnt = 0
        for l in f:
            if l.startswith('%') or l.startswith('\n'):
                continue
            assert(d.variables[cnt].latexcode() + '\n' == l)
            cnt = cnt + 1

def test_document():
    # Basic method
    d = Document()
    d.setvariable(Variable('name1', 'value1'))
    assert(d.variables[0].name == 'name1' and d.variables[0].value == 'value1')
    d.setvariable(Variable('name2', 'value2'))
    d.setvariable(Variable('name2', 'value3'))
    assert(d.variables[1].name == 'name2' and d.variables[1].value == 'value3')
    
    # Fail inserting not Variable
    try:
        d.setvariable("string")
    except TypeError:
        pass
        
    # Saving
    d.save('test.tmp')
    check_file_with_document(d, 'test.tmp')
    
    d.clearvariables()
    assert(len(d.variables) == 0)
    d.setvariable(Decimal("R", 3423.34768, 6))
    d.save('test.tmp')
    check_file_with_document(d, 'test.tmp')
    
    
    
