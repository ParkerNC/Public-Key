from random import randrange
from random import getrandbits

# Pre generated primes
primelist = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]

def fastexp(b: int, e: int, n: int) -> int:
    prod = 1
    base = b
    exp = bin(e)[::-1]
    exp = exp[:-2]
    for bit in exp:
        if bit == "1":
            prod = (prod * base) %n
        
        base = (base * base ) %n

    return prod

def millerR(p: int, i: int) -> bool:
    s = 0
    n = p
    d = n-1
    while(d%2 == 0):
        s += 1
        d = d >> 1

    for r in range(i):
        prime = False
        a = randrange(2, n-2)
        x = fastexp(a, d, n)
        if x == 1 or x == (n-1):
            continue
        for step in range(s-1):
            x = fastexp(x, 2, n)
            if x == (n-1):
                prime = True
                break
        
        if prime:
            continue

        return False

    return True


def primeGen(bitlen: int) -> int:
    qlen = bitlen-1
    while(1):
        test = randrange(2**(qlen-1)+1, 2**qlen-1)
        if not test & 1:
            continue

        for prime in primelist:
            if test % prime == 0:
                continue


        if millerR(test, 10):
            test = (test << 1) + 1

            if millerR(test, 10):
                print(test)
                return test

    return test

        

if __name__ == "__main__":
    b = 4235880211405804673
    e = 131
    n = 12855544647099734480

    #res = fastexp(b, e, n)
    tmp = millerR(175118011353974613747414115745586823026539540640072921440880723823673023327752553018161242200813211305556829955825029953131751251477020252777664395370693866564432656651061844109313776792589236703517908150685842487470642697808561061731352854662829518025487893728617216219673621722830025917527599882791614689407, 20)

    x = primeGen(1024)
    #print(x)
