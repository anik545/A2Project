import unittest
from app.pyscripts.complex_loci import parse, get_implicit

class TestComplexLoci(unittest.TestCase):

    def test_parse(self):
        """Tests to parse individual parts of an expression."""

        self.assertEqual(parse('|z|').replace(' ', ''), 'sqrt(x**2+y**2)')

        self.assertEqual(parse('arg(z)').replace(' ', ''),
                         '2*atan((-x+sqrt(x**2+y**2))/y)')

        self.assertEqual(parse('|z+1-3i|').replace(' ', ''),
                         'sqrt((x+1)**2+(y-3)**2)')

        self.assertEqual(parse('arg(z+5-2i)').replace(' ', ''),
                         '2*atan((-x+sqrt((x+5)**2+(y-2)**2)-5)/(y-2))')

    def test_get_lines(self):
        """Tests the creation of full equations from input."""

        self.assertEqual(get_implicit('|z|=|z-1|').replace(' ', ''),
                         'sqrt(x**2+y**2)-sqrt(y**2+(x-1)**2)=0')

        self.assertEqual(get_implicit('|z-2i|=2*|z+1|').replace(' ', ''),
                         'sqrt(x**2+(y-2)**2)-2*sqrt(y**2+(x+1)**2)=0')

        self.assertEqual(get_implicit('arg(z)=arg(z-1)+pi/4').replace(' ', ''),'-2*atan((x-sqrt(x**2+y**2))/y)-2*atan((-x+sqrt(y**2+(x-1)**2)+1)/y)-pi/4=0')

        self.assertEqual(get_implicit('arg(z-i)>=pi/4').replace(' ',''), '-2*atan((x-sqrt(x**2+(y-1)**2))/(y-1))-pi/4>=0')

        self.assertEqual(get_implicit('|z|<4').replace(' ', ''), 'sqrt(x**2+y**2)-4<0')

unittest.main()
