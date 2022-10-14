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
    print(shared)

    #print(len(bin(shared)))

    inp = shared.to_bytes(128, 'big') or b'\0'

    sharedKey = SHA256.new(inp)
    print(sharedKey.hexdigest()[:16])
    return sharedKey.digest()[:16]

def AES_CBC(key: bytes, iv: int, ciptext: str):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(ciptext, AES.block_size)


if __name__ == "__main__":
    b = 4235880211405804673
    e = 131
    n = 12855544647099734480

    diffieCyper = "8ce3c3a667b2b4e201b9298be61f732f60606cb21285a639cbddf0556c6afa6f3d5d77a99dafe5d483934a07794e8294417f07a8a268d1ee3610d72ff576cfd397dd808bae9728b9a93983b81c67ae0347d7ee028e3381cbbbfd14932a9d7a54db3923c7166aabf5468527643ddda44b6c072e0b2924afee19d01eae8fbb2603788e810610353aec697188e2f4360332f8433a125158ecbac280aff14f2475b1"
    iv = "832130f4d7e6aad1229c1f2efc388057"

    modp = 140274374150807592491449133255658231264268770631566034386022222100531343719074131494320604278312778732859456385125624162933502046700948579578441334754582148485091680383613071507321333900217883755516757499505617257396578048774303326718471426859340410626824475827439545034654263158357112035471608065055234954703
    givenPublicKey = 113033952057894117566443321716439522084058991655107417073586372343605145021721352719800447970481255648045029179651417037482054531349619634402473181246738318584503180422493895492958426157100825366234722997873835312843273813921183709256928345774710218921353493607216571399195900819084116447647618932508437273390
    myPublicKey = 36491309120849954296958091243249826996991977319692712264754839564668213405948713295933907354617459495027626161347499338478592345879927234815786320421135533651825768726343873448175045721289621577632848909009584383507869277602080088928570644952951253215632431532865692797799215656708146935892211943041899278759

    #res = fastexp(b, e, n)
    #tmp = millerR(175118011353974613747414115745586823026539540640072921440880723823673023327752553018161242200813211305556829955825029953131751251477020252777664395370693866564432656651061844109313776792589236703517908150685842487470642697808561061731352854662829518025487893728617216219673621722830025917527599882791614689407, 20)

    #x = primeGen(1024)
    #x = primeGen(1024)
    #print(x)

    #print(diffe_helman_pk(140274374150807592491449133255658231264268770631566034386022222100531343719074131494320604278312778732859456385125624162933502046700948579578441334754582148485091680383613071507321333900217883755516757499505617257396578048774303326718471426859340410626824475827439545034654263158357112035471608065055234954703, 5))

    x = diffe_helman_decrypt(myPublicKey, givenPublicKey, modp)
    