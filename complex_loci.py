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
    print(inner)
    x,y=symbols('x y',real=True)
    locs={'x':x,'y':y}
    in_eq = sympify(inner,locs)
    return str(2*atan((sqrt(re(in_eq)**2+im(in_eq)**2)-re(in_eq))/im(in_eq)))


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

    if 'arg' in eq:
        a,b = eq.find('arg(')+4,eq.find('arg(')+4
        found=0
        while found>=0:
            found += 1 if eq[b]=='(' else 0
            found -= 1 if eq[b]==')' else 0
            b+=1
        eq = eq[:a-4] + parse_arg(eq[a:b-1]) + eq[b:]

    return eq

def get_implicit(lhs,rhs,latx=False):

    x,y=symbols('x y',real=True)
    locs={'x':x,'y':y}

    lhs=parse(lhs)
    lhs=sympify(lhs,locals=locs)

    rhs=parse(rhs)
    rhs=sympify(rhs,locals=locs)

    eq = lhs-rhs
    eq = eq.simplify()
    if latx:
        return ((latex(eq))+'=0').replace('atan','arctan')
    else:
        pprint(eq)
        return str(eq)+'=0'

if __name__ == '__main__':
    #a = parse_arg('x+y*I/(x+y*I-4)')
    #print(a)
    t1=time.time()
    b=get_implicit('arg(z)','pi/4',latx=True)
    t2=time.time()
    print(b)
    pprint(b)
    print('time: ',t2-t1,' seconds')
    #print(complexify(LHS+'-'+RHS))
