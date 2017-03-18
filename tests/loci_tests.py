import unittest
from app.pyscripts.complex_loci import parse, get_implicit

class TestComplexLoci(unittest.TestCase):

    #Tests to parse individual parts of an expression.
    def test_parse_modulus(self):
        self.assertEqual(parse('|z|').replace(' ', ''), 'sqrt(x**2+y**2)')
        self.assertEqual(parse('|z+1-3i|').replace(' ', ''),
                 'sqrt((x+1)**2+(y-3)**2)')

    def test_parse_argument(self):
        self.assertEqual(parse('arg(z)').replace(' ', ''),
                         '2*atan((-x+sqrt(x**2+y**2))/y)')

        self.assertEqual(parse('arg(z+5-2i)').replace(' ', ''),
                 '2*atan((-x+sqrt((x+5)**2+(y-2)**2)-5)/(y-2))')

    def test_implicit_multiply(self):
        self.assertEqual(parse('3z+2pi+3i'), '3*(x+y*I)+2*pi+3*I')

    #Tests the creation of full equations from input
    def test_get_equation_line(self):
        self.assertEqual(get_implicit('|z|-|z-1|=5').replace(' ', ''),
                         'sqrt(x**2+y**2)-sqrt(y**2+(x-1)**2)-5=0')

    def test_get_equation_circle(self):
        self.assertEqual(get_implicit('|z-2i|=2*|z+1|').replace(' ', ''),
                         'sqrt(x**2+(y-2)**2)-2*sqrt(y**2+(x+1)**2)=0')

    def test_get_equation_arc(self):
        self.assertEqual(get_implicit('arg(z)-arg(z-1)=pi/4').replace(' ', ''),
        '-2*atan((x-sqrt(x**2+y**2))/y)-2*atan((-x+sqrt(y**2+(x-1)**2)+1)/y)-pi/4=0')

    #Tests the creation of full inequalities from input
    def test_get_inequality_half_line(self):
        self.assertEqual(get_implicit('arg(z-i)>=pi/4').replace(' ',''),
        '-2*atan((x-sqrt(x**2+(y-1)**2))/(y-1))-pi/4>=0')

    def test_get_inequality_circle(self):
        self.assertEqual(get_implicit('|z|<4').replace(' ', ''),
        'sqrt(x**2+y**2)-4<0')

    def test_get_latex(self):
        self.assertEqual(get_implicit('arg(z+i)+|z-1|=1',latx=True).replace(' ', ''), '\\sqrt{y^{2}+\\left(x-1\\right)^{2}}-2\\operatorname{arctan}{\\left(\\frac{1}{y+1}\\left(x-\\sqrt{x^{2}+\\left(y+1\\right)^{2}}\\right)\\right)}-1=0')

unittest.main()
