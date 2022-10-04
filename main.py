from sys import argv
from multiplicative import *

'''
Output utility functions.
'''
def D2str(D):
    res = ''
    for idx, i in enumerate(D):
        if idx >= len(D)-1:
            res += f'Z_{i}'
        else:
            res += f'Z_{i} × '
    return res

def elem2sym(R):
    if R==(0,)*g: return '0'
    if R==G(g-1): return '1'
    res = 0
    cumprod = 1
    i = g-1
    while i >= 0:
        res += R[i] * cumprod
        cumprod *= D[i]
        i -= 1
    return chr(ord('a')+res-2)

def printtables():
    print('+ ' + ' '.join(elem2sym(R) for R in elements()) + ' '*4 +
          '* ' + ' '.join(elem2sym(R) for R in elements()))
    for R in elements():
        print(f'{elem2sym(R)} ' + ' '.join(elem2sym(add(R,S)) for S in elements()) + ' '*4 +
              f'{elem2sym(R)} ' + ' '.join(elem2sym(mul(R,S)) for S in elements()))


total = 0
# counts the number of valid multiplicative structures have certain properties
# {D: [# valid M, # commutative M, # M that are domains, # M that have idempotents]}
counts = {}
output = True

while True:
    try:
        n = int(input('n = '))
    except ValueError:
        continue
    else:
        break

for D in divseqs(n):
    D, g = tuple(D), len(D)
    setD(D)
    total = 0
    counts.update({D: [0,0,0,0]})
    if g == 1:
        counts.update({D: [1,1, isprime(n), 1-isprimepow(n)]})
        continue
    print(f'Checking {(n**((g-1)**2))} possibilities for additive group {D2str(D)}')
    for M in multables():
        setM(M)
        total += 1
        if total%1000==0:
            print(total)
        if checkassoc() and checkdistrib():
            #sanity_check()
            comm, domain, idempotents = checkprops()
            counts[D][0] += 1
            counts[D][1] += comm
            counts[D][2] += domain
            counts[D][3] += len(idempotents)>=1
            print(total)

            prop_str = ''
            if comm: prop_str += 'commutative '
            if domain: prop_str += 'domain '
            if len(idempotents) >= 1:
                if comm or domain:
                    prop_str += 'w/ idempotents '
                else:
                    prop_str += 'has idempotents '
                prop_str += ' '.join(elem2sym(R) for R in idempotents)
            print(prop_str)

            if output:
                printtables()
                print()

print('I found:')
for D, (count, comms, domains, idempotents) in counts.items():
    print(f'{count}/{n**((len(D)-1)**2)} rings with additive group {D2str(D)} ' +
          f'({comms} commutative, {domains} domains, {idempotents} with idempotents)')
print('NOT up to isomorphism!')
