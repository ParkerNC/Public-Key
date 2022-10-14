from random import randrange
from random import getrandbits

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256

from sys import byteorder

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
                return test

    return test

def diffe_helman_pk(p: int, g: int) -> int:
    a = randrange(p)
    pKey = fastexp(g, a, p)

    return pKey

def diffe_helman_decrypt(mykey: int, theykey: int, mod: int) -> int:
    shared = fastexp(theykey, mykey, mod)

    print(len(bin(shared)))

    inp = shared.to_bytes(128, 'big') or b'\0'

    sharedKey = SHA256.new(inp)
    print(sharedKey.hexdigest()[:16])
    return 

if __name__ == "__main__":
    b = 4235880211405804673
    e = 131
    n = 12855544647099734480

    #res = fastexp(b, e, n)
    #tmp = millerR(175118011353974613747414115745586823026539540640072921440880723823673023327752553018161242200813211305556829955825029953131751251477020252777664395370693866564432656651061844109313776792589236703517908150685842487470642697808561061731352854662829518025487893728617216219673621722830025917527599882791614689407, 20)

    #x = primeGen(1024)
    #x = primeGen(1024)
    #print(x)

    #print(diffe_helman_pk(140274374150807592491449133255658231264268770631566034386022222100531343719074131494320604278312778732859456385125624162933502046700948579578441334754582148485091680383613071507321333900217883755516757499505617257396578048774303326718471426859340410626824475827439545034654263158357112035471608065055234954703, 5))

    x = diffe_helman_decrypt(56654555966771266523190387585086590153540531186220900266733322999098832806571528480332578582787087440173873037738260857794459156475069579722674358032738366239512020195567769587656276321541424853261647401916756216098965581260389765192787429458289849142750600348866946446474202450152180440921875235009598170374, 66035218161690652442223114304019727450288343180438652538722619873593366757251257950388652616990869529724663792521396579899071353425903818908714220815669672763696986848304584769169563754296398927524251549639108309897757103930785659266686915331655399324366414653535071877071592952071622782838588924906957905059, 140274374150807592491449133255658231264268770631566034386022222100531343719074131494320604278312778732859456385125624162933502046700948579578441334754582148485091680383613071507321333900217883755516757499505617257396578048774303326718471426859340410626824475827439545034654263158357112035471608065055234954703)