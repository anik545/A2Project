from sympy import *
import time

#TODO instead of subbing Abs(), find sqrt(re(x)+im(x)) instead.
def mod_to_abs(eq):
    eq_list=[str(x) for x in eq]
    if '|' not in eq:
        return eq
    for x,char in enumerate(eq_list):
        if char=='|':
            eq_list[x]='Abs('
            for y,char2 in reversed(list(enumerate(eq))):
                if char2=='|':
                    eq_list[y]=')'
                    return ''.join(eq_list[:x+1] + list(mod_to_abs(eq_list[x+1:y])) + eq_list[y:])

def parse_arg(inner):
    z=Symbol('Z',real=False)
    locs={'Z':z}
    sympify(eq,locs)


def parse(eq):
    eq=mod_to_abs(eq)
    eq=eq.replace('z','Z')
    eq_list=list(eq)
    eq_list=['I' if ch=='i' and eq_list[n-1] not in ['p','P'] else ch for n,ch in enumerate(eq_list)]
    nums=['1','2','3','4','5','6','7','8','9','0']
    for n,ch in enumerate(eq_list):
        if (ch=='Z' or ch=='I' or ch=='A') and (eq_list[n-1] in nums):
            eq_list.insert(n,'*')
    eq=''.join(eq_list)
    eq=eq.replace('Z','(x+y*I)')

    return eq


#TODO add support for arg, use equation: 2atan((sqrt(x^2+y^2)-x)/y)

def get_lines(lhs,rhs):

    x,y=symbols('x y',real=True)
    locs={'x':x,'y':y}

    #LHS
    lhs=parse(lhs)
    lhs=sympify(lhs,locals=locs)
    print(lhs)

    #RHS
    rhs=parse(rhs)
    rhs=sympify(rhs,locals=locs)
    print(rhs)

    solns=list(solve(lhs-rhs,locs['y']))
    if solns:
        typ='func'
    else:
        solns=list(solve(lhs-rhs,locs['x']))
        solns=[float(x) for x in solns]
        typ='vert'
    return typ,solns


#TODO figure out when the input is this type of equation
#maybe evaluate everything inside arg, sympify, if div
def get_line_simple_arg(lhs,rhs):
    lhs,rhs=parse(lhs),parse(rhs)
    if 'arg' in lhs:
        lhs=lhs.replace('arg((','').replace(')','')
        angle=sympify(rhs)
        expr=sympify(lhs).subs('x',0).subs('y',0)
    else:
        rhs=rhs.replace('arg(','').replace(')','')
        angle=sympify(lhs)
        expr=sympify(rhs).subs('x',0).subs('y',0)
    p1=[float(-re(expr)),float(-im(expr))]
    print(p1,angle)
    x,y=symbols('x y',real=True)
    solns_dict=solve([atan2(y,x)-angle,x**2+y**2-1])
    p2=[float(solns_dict[0][x]+p1[0]),float(solns_dict[0][y]+p1[1])]
    print(p1,p2)
    return (p1,p2)


if __name__ == '__main__':
    equation="2|z-5i|=2|z-5|"
    LHS,RHS=equation.split('=')
    t1=time.time()
    lines=get_lines(LHS,RHS)
    t2=time.time()
    print(t2-t1,'ms')
    print(lines)

    #print(complexify(LHS+'-'+RHS))
