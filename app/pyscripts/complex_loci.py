from sympy import symbols, re, im, sqrt, atan, sympify, latex

# TODO instead of subbing Abs(), find sqrt(re(x)+im(x)) instead.


def parse_mod(inner):
    """Convert expression inside modulus to x-y equation."""
    # Set up sympy variables and convert inner expression to sympy object
    x, y = symbols('x y', real=True)
    locs = {'x': x, 'y': y}
    in_eq = sympify(inner, locs)
    # Return string version of formula with real and imaginary parts substituted
    return str(sqrt(im(in_eq)**2 + re(in_eq)**2))


def parse_arg(inner):
    """Convert expression inside arument function to x-y equation."""
    # Set up sympy variables and convert inner expression to sympy object
    x, y = symbols('x y', real=True)
    locs = {'x': x, 'y': y}
    in_eq = sympify(inner, locs)
    # Return string version of formula with real and imaginary parts substituted
    return str(2 * atan((sqrt(re(in_eq)**2 + im(in_eq)**2) - re(in_eq)) / im(in_eq)))


def parse(eq):
    """Return string of manipulated equation."""
    eq = eq.replace('z', 'Z').replace('^', '**')
    # Make the string a list for easier manipulation
    eq_list = list(eq)
    # Sympy recognises uppercase I as sqrt(-1)
    # Any isolated i's (not within another word like pi) should be converted to uppercase
    eq_list = ['I' if ch == 'i' and eq_list[n - 1]
               not in ['p', 'P', 's', 'S'] else ch for n, ch in enumerate(eq_list)]
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    # Insert a * after a number and before a letter, bracket or modulus sign
    # Allows users enter 2z to mean 2 * z
    for n, ch in enumerate(eq_list):
        if (ch in ['Z', 'I', 'A', 'a', 'p', 'P', '(']) and (eq_list[n - 1] in nums) and n > 0:
            eq_list.insert(n, '*')
    # Convert back into string
    eq = ''.join(eq_list)
    # Substitute z for x+yi
    eq = eq.replace('Z', '(x+y*I)')

    # While there are still modulus lines
    while '|' in eq:
        # Find first modulus line
        a = eq.find('|')
        # Find matching line
        b = eq.find('|', a+1)
        # Parse everything between modulus lines according to formula
        eq = eq[:a] + parse_mod(eq[a + 1:b]) + eq[b + 1:]

    # While there is still an argument funcion in the equation
    while 'arg(' in eq:
        # Find occurence of function
        # a is the index of the start of the inner expression
        # Also initialise b to this value
        a, b = eq.find('arg(') + 4, eq.find('arg(') + 4
        # Find correct enclosing bracket
        found = 0
        while found >= 0:
            # Add 1 if open bracket, subtract 1 if close bracket
            found += 1 if eq[b] == '(' else 0
            found -= 1 if eq[b] == ')' else 0
            # Increment counter
            b += 1
            # When found is less than 0, then the correct close bracket is found
        # Parse everything between modulus lines according to formula
        eq = eq[:a - 4] + parse_arg(eq[a:b - 1]) + eq[b:]
    return eq

def parse_inequality(eq):
    """Return type of (in)equality as string"""
    if '<=' in eq:
        return '<='
    elif '>=' in eq:
        return '>='
    elif '>' in eq:
        return '>'
    elif '<' in eq:
        return '<'
    else:
        return '='

def get_implicit(eq, latx=False):
    """Return implicit equation in x and y"""
    # Get the type of (in)equality the expression is
    op = parse_inequality(eq)
    # Split it up depending on the type of expression
    lhs, rhs = eq.split(op)

    # Set up symbols
    x, y = symbols('x y', real=True)
    locs = {'x': x, 'y': y}
    # Parse both the left and right hand side
    # Convert to sympy objects based on set up variables
    lhs = parse(lhs)
    lhs = sympify(lhs, locals=locs)

    rhs = parse(rhs)
    rhs = sympify(rhs, locals=locs)

    # Put equation in the form f(x,y)=0 and simplify
    eq = lhs - rhs
    eq = eq.simplify()
    if latx:
        # Convert to format desmos understands (latex)
        return ((latex(eq)) + ''+op+' 0').replace('atan', 'arctan')
    else:
        return str(eq) + op + '0'


if __name__ == '__main__':
    print(parse('arg(z+1)-arg(z-1)'))
