from pydoc import plain
from random import randrange
from random import getrandbits

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
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
        #test = getrandbits(qlen)
        print(len(bin(test)))
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
    print(a)
    pKey = fastexp(g, a, p)

    return pKey

def diffe_helman_decrypt(mykey: int, theykey: int, mod: int) -> int:
    shared = fastexp(theykey, mykey, mod)
    
    print(shared)

    inp = shared.to_bytes((shared.bit_length() + 7) // 8, 'big') or b'\0'

    sharedKey = SHA256.new(inp)
    
    print(sharedKey.hexdigest()[:16])

    return sharedKey.hexdigest()[:16]

def AES_CBC(key: str, iv: str, ciptext: str):
    
    ivhex = bytes.fromhex(iv)
    hexkey = bytes.fromhex(key)
    print(ivhex, hexkey)
    hexCiph = bytearray.fromhex(ciptext)
    cipher = AES.new(hexkey, AES.MODE_CBC, ivhex)

    plaintext = cipher.decrypt(hexCiph)
    plaintext = plaintext.decode("utf-8")

    print(plaintext)


if __name__ == "__main__":
    b = 4235880211405804673
    e = 131
    n = 12855544647099734480

    diffieCyper = "8ce3c3a667b2b4e201b9298be61f732f60606cb21285a639cbddf0556c6afa6f3d5d77a99dafe5d483934a07794e8294417f07a8a268d1ee3610d72ff576cfd397dd808bae9728b9a93983b81c67ae0347d7ee028e3381cbbbfd14932a9d7a54db3923c7166aabf5468527643ddda44b6c072e0b2924afee19d01eae8fbb2603788e810610353aec697188e2f4360332f8433a125158ecbac280aff14f2475b1"
    iv = "eb85c14b4322fd956cdd18c5f71b63e2"

    modp = 140274374150807592491449133255658231264268770631566034386022222100531343719074131494320604278312778732859456385125624162933502046700948579578441334754582148485091680383613071507321333900217883755516757499505617257396578048774303326718471426859340410626824475827439545034654263158357112035471608065055234954703
    givenPublicKey = 71503360547177244740871942427934802985954203769739168256253280874398044896324692565878166840147272532330237262077009270799636696469289654708093477979546298132232678185155496081943966934546205158497059581363680011826828777898460511295730285433585080824477042511272411533777299063743524338465535582730637685352
    myPublicKey = 36491309120849954296958091243249826996991977319692712264754839564668213405948713295933907354617459495027626161347499338478592345879927234815786320421135533651825768726343873448175045721289621577632848909009584383507869277602080088928570644952951253215632431532865692797799215656708146935892211943041899278759
    myPrivateKey = 132123520252965958236047294614393942200618160823485792582500127805465457366689342433688117704177896395359914799433372311016250231089183959563022363134457709707460190238467691979259887605883739428051182749629933510380291494746116158386529987607453088300501928891618829605021434112322436997144940498761457141473

    #res = fastexp(b, e, n)
    #tmp = millerR(175118011353974613747414115745586823026539540640072921440880723823673023327752553018161242200813211305556829955825029953131751251477020252777664395370693866564432656651061844109313776792589236703517908150685842487470642697808561061731352854662829518025487893728617216219673621722830025917527599882791614689407, 20)

    #x = primeGen(1024)
    #x = primeGen(1024)
    #print(x)

    #print(diffe_helman_pk(modp, 5))
    x = diffe_helman_decrypt(myPrivateKey, givenPublicKey, modp)
    AES_CBC(x, iv, diffieCyper)
    