'''
Rings of order n are generated according to additive structure. Each
additive structure is represented by a divisibility sequence D = [x_1,
..., x_k] of length g (for 'generator'), and the ring elements are
represented as g-tuples (think of them as elements of the direct sum
\oplus_i Z_{x_i}, so the components are taken mod x_i).

The generators are the 'standard basis vectors' (1,0,0,...),
(0,1,0,...), and so on. Each multiplicative structure is represented
as a dictionary M mapping pairs of generators to arbitrary g-tuples.
The last generator (0,...,0,1) is reserved for the multiplicative
identity.
'''

from itertools import product
from additive import *

D = []
g = 0
M = {}

def setD(_D):
    global D, g
    D, g = _D, len(_D)

def setM(_M):
    global M
    M = _M

'''Return the ith generator (...,0,1,0,...).'''
def G(i):
    return tuple(int(x==i) for x in range(g))

'''The variables I, J, K, R, S, ... are used for ring elements.'''
def add(R, S):
    return tuple((R[i]+S[i])%D[i] for i in range(g))

def smul(k, R):
    return tuple((k*R[i])%D[i] for i in range(g))

def mul(R, S):
    res = (0,)*g
    for i, a in enumerate(R):
        for j, b in enumerate(S):
            res = add(res, smul(a*b, M[(G(i),G(j))]))
    return res

'''Iterate through all ring elements, i.e. g-tuples.'''
def elements():
    for L in product(*tuple(range(i) for i in D)):
        yield L

'''Iterate through all multiplicative structures.'''
def multables():
    for L in product(elements(), repeat=(g-1)**2):
        table = {}
        for i in range(0,g):
            for j in range(0,g):
                I, J = G(i), G(j)
                # first two branches are to handle the identity
                if i==g-1:
                    table.update({(I,J): J})
                elif j==g-1:
                    table.update({(I,J): I})
                else:
                    K = L[i*(g-1) + j]
                    table.update({(I,J): K})
        yield table

def checkassoc():
    for i,j,k in product(range(g), repeat=3):
        I, J, K = G(i), G(j), G(k)
        if mul(mul(I,J),K) != mul(I,mul(J,K)):
            return False
    else:
        return True

def checkdistrib():
    for i,j in product(range(g), repeat=2):
        I, J = G(i), G(j)
        if smul(D[i], mul(I,J)) != (0,)*g or \
           smul(D[i], mul(J,I)) != (0,)*g:
            return False
    else:
        return True

'''
These are sanity check function to ensure that the shortcuts taken by
`checkassoc` and `checkdistrib` still give correct results.
'''
def checkassoc_full():
    for R,S,T in product(elements(), repeat=3):
        if mul(mul(R,S),T) != mul(R,mul(S,T)):
            return False
    else:
        return True

def checkdistrib_full():
    for R,S,T in product(elements(), repeat=3):
        if mul(add(R,S),T) != add(mul(R,T),mul(S,T)) or \
           mul(R,add(S,T)) != add(mul(R,S),mul(R,T)):
            return False
    else:
        return True

'''
Assuming M is a valid multiplicative structure, find out some properties of
M like commutativity.
'''
def checkprops():
    comm, domain, idempotents = 1,1,[]
    for R in elements():
        if mul(R,R) == R and R != (0,)*g and R != G(0):
            idempotents.append(R)
        for S in elements():
            if mul(R,S) != mul(S,R):
                comm = 0
            if mul(R,S) == (0,)*g and R != (0,)*g and S != (0,)*g:
                domain = 0
    return (comm, domain, idempotents)

'''If I ever need to be doubly sure that my algorithm works...'''
def sanity_check():
    if not checkassoc_full() or not checkdistrib_full():
        print('ARGHHHH!!')
        exit()
    print('things seem alright...')

