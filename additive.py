'''
Functions to calculate the possible additive structures of an order
n ring. Each additive structure, an abelian group, corresponds to a
direct sum of cyclic groups of order Z_{x_i}, where (x_1,...,x_k) is a
sequence such that x_{i+1} divides x_i and whose product is n. I call
such a k-tuple a **divisibility sequence**---the relevant function is
`divseqs`.
'''

from itertools import product
from math import sqrt

def smallestfactor(n):
    d = 2
    for d in range(2,n//2+1):
        if n%d == 0: return d
    else:
        return n

def isprime(n):
    for i in range(2,int(sqrt(n))+1):
        if n%i==0:
            return 0
    return 1

'''
Return a dictionary {p: m}, where p runs through the prime factors of n
and m is the corresponding multiplicity.
'''
def factorize(n):
    if n==1:
        return dict()
    d = smallestfactor(n)
    factors = factorize(n//d)
    if d in factors.keys():
        factors[d] += 1
    else:
        factors.update({d: 1})
    return factors

def isprimepow(n):
    return len(factorize(n).keys()) == 1

def _partitions(n,k):
    if n==0:
        yield []
    for i in range(k,n+1):
        for P in _partitions(n-i,i):
            yield [i]+P

'''
Iterate through lists of positive integers [x_1, ..., x_k]
such that 1 <= x_1 <= ... <= x_k and \sum x_i = n.
'''
def partitions(n):
    return _partitions(n,1)

'''
Iterate through the dictionaries {p: P} where p runs through the prime
factors of n and P is some partition of its multiplicity m.
'''
def factorpartitions(n):
    factors = factorize(n)
    L = tuple(factors.keys())
    gen = product(*tuple(
        partitions(factors[p]) for p in L
    ))
    for fp in gen:
        yield {L[p]: P for p, P in enumerate(fp)}

'''
Given a dictionary fp = {p: P} associating prime factors with partitions of
its multiplicity, greedily generate a divisibility sequence (x_1, ..., x_k).
'''
def divseq(fp):
    seq = []
    L = list(fp.keys())
    while True:
        if not fp.keys():
            # all keys deleted, meaning all numbers generated
            break
        cur = 1
        for p in L:
            # the key was deleted halfway
            if p not in fp.keys():
                continue
            P = fp[p]
            max_idx = P.index(max(P))
            cur *= p**P[max_idx]
            if len(P) > 1:
                del fp[p][max_idx]
            else:
                del fp[p]
        seq.append(cur)
    return seq

'''
Iterates through all divisiblity sequences for n.
'''
def divseqs(n):
    # The reversing is so that we can use (0,...,0,1) as the multiplicative
    # unit, since its additive order must be the greatest element of the
    # divisibility sequence.
    return map(lambda fp: list(reversed(divseq(fp))), factorpartitions(n))
