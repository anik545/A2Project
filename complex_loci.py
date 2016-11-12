from sympy import *
import time

# TODO instead of subbing Abs(), find sqrt(re(x)+im(x)) instead.


def parse_mod(inner):
    x, y = symbols('x y', real=True)
    locs = {'x': x, 'y': y}
    in_eq = sympify(inner, locs)
    return str(sqrt(im(in_eq)**2 + re(in_eq)**2))


def parse_arg(inner):
    x, y = symbols('x y', real=True)
    locs = {'x': x, 'y': y}
    in_eq = sympify(inner, locs)
    return str(2 * atan((sqrt(re(in_eq)**2 + im(in_eq)**2) - re(in_eq)) / im(in_eq)))


def parse(eq):
    eq = eq.replace('z', 'Z').replace('^', '**')
    eq_list = list(eq)
    eq_list = ['I' if ch == 'i' and eq_list[n - 1]
               not in ['p', 'P'] else ch for n, ch in enumerate(eq_list)]
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for n, ch in enumerate(eq_list):
        if (ch in ['Z', 'I', 'A', 'a', 'p', 'P','(']) and (eq_list[n - 1] in nums) and n > 0:
            eq_list.insert(n, '*')
    eq = ''.join(eq_list)
    eq = eq.replace('Z', '(x+y*I)')

    if '|' in eq:
        a = eq.find("|")
        b = eq.find('|', a + 1)
        eq = eq[:a] + parse_mod(eq[a + 1:b]) + eq[b + 1:]

    if 'arg' in eq:
        a, b = eq.find('arg(') + 4, eq.find('arg(') + 4
        found = 0
        while found >= 0:
            found += 1 if eq[b] == '(' else 0
            found -= 1 if eq[b] == ')' else 0
            b += 1
        eq = eq[:a - 4] + parse_arg(eq[a:b - 1]) + eq[b:]
    return eq


def get_implicit(lhs, rhs, latx=False):

    x, y = symbols('x y', real=True)
    locs = {'x': x, 'y': y}

    lhs = parse(lhs)
    lhs = sympify(lhs, locals=locs)

    rhs = parse(rhs)
    rhs = sympify(rhs, locals=locs)

    eq = lhs - rhs
    eq = eq.simplify()
    if latx:
        return ((latex(eq)) + ' = 0').replace('atan', 'arctan')
    else:
        return str(eq) + '=0'

if __name__ == '__main__':
    t1 = time.time()
    b = get_implicit('arg(z)', 'pi/4', latx=True)
    t2 = time.time()
    print(b)
    pprint(b)
    print('time: ', t2 - t1, ' seconds')
