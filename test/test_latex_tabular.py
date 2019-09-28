
from LabTools.latex import TabularContent, TabularColumn
from LabTools.utils import unarray
import filecmp, numpy

a_v = numpy.array([2., 3.])
a_u = numpy.array([0.2, 0.3])
b_v = numpy.array([2., 3., 4.])
b_u = numpy.array([0.2, 0.3, 0.4])
    

def test_empty_file_tabular():
    tc = TabularContent()
    tc.save('test.tmp')
    assert(filecmp.cmp('test/outputs/empty_tabular.tex', 'test.tmp'))
    
def test_basic_tabular():
    # Basic arrays for twsting
    tc = TabularContent()
    c1 = TabularColumn(a_v)
    c2 = TabularColumn(b_v)
    tc.add_column(c1)
    tc.add_column(c2)
    tc.save('test.tmp')
    assert(filecmp.cmp('test/outputs/basic_table.tex', 'test.tmp'))
    
def test_column():
    tc = TabularContent()
    c1 = TabularColumn(a_v, global_unc = 6.0)
    c2 = TabularColumn(unarray(b_v, b_u), show_unc  = False)
    c3 = TabularColumn(a_v, value_digits = 1)
    c4 = TabularColumn(unarray(a_v, a_u))
    c5 = TabularColumn(unarray(b_v, b_u), unc_digits=3)
    tc.add_column(c1)
    tc.add_column(c2)
    tc.add_column(c3)
    tc.add_column(c4)
    tc.add_column(c5)
    tc.save('test.tmp')
    assert(filecmp.cmp('test/outputs/test_column.tex', 'test.tmp'))
