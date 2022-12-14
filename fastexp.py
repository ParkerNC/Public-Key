
#Parker Collier
#public key
#using 1 late day
#go vols 

from random import randrange

from Crypto.Cipher import AES

from Crypto.Hash import SHA256

#used to speed up prime gen
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
    #part 1 fast modular exponentiation
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
    #part 2 miller robin implementation
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


def safePrimeGen(bitlen: int) -> int:
    qlen = bitlen-1
    #safe prime gen for diffie helman with a few optimizations, ie checking ez primes and making sure even
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
    #generates a prvate key number for diffie helman
    a = randrange(p)
    print(a)
    pKey = fastexp(g, a, p)

    return pKey

def diffe_helman_decrypt(mykey: int, theykey: int, mod: int) -> int:
    shared = fastexp(theykey, mykey, mod)
    
    #prints the found number for shared key
    print(shared)

    inp = shared.to_bytes((shared.bit_length() + 7) // 8, 'big') or b'\0'

    sharedKey = SHA256.new(inp)
    
    #print(sharedKey.hexdigest()[:16])

    #returns sha hash of shared key
    return sharedKey.digest()[:16]

def AES_CBC(key: bytes, iv: str, ciptext: str):
    #decrypts using given iv, ciphertext, and generted SHA key, also fudges with the bits a bit to get big endian 
    bitIv = int(iv, 16)
    print(bitIv)
    bitIv = bitIv.to_bytes((bitIv.bit_length() + 7) // 8, 'big') or b'\0'
    
    bitCiph = int(ciptext, 16)
    bitCiph = bitCiph.to_bytes((bitCiph.bit_length() + 7) // 8, 'big') or b'\0'

    cipher = AES.new(key, AES.MODE_CBC, bitIv)

    plaintext = cipher.decrypt(bitCiph)

    plaintext = plaintext.decode("utf-8")

    print(plaintext)

def RSA_gen(len: int, e: int = 65537):
    #generates a prime, and then generates more primes untill they satisty RSA gcd(n) constraints
    i = 0
    p = 1
    q = 1
    while(gcd(e, ((q-1)  * (p-1))) != 1):
        test = randrange(2**(len-1)+1, 2**len-1)
        if not test & 1:
            continue

        for prime in primelist:
            if test % prime == 0:
                continue


        if millerR(test, 10):
            if i == 0:
                p = test
            else:
                q = test
            i += 1
        

    return p, q

def gcd(a: int, b: int) -> int:
    #taken from the notes
    tmpA = a
    tmpB = b
    while tmpB != 0:
        tmpA, tmpB = tmpB, tmpA % tmpB

    return tmpA

def EEMI(e: int, n: int) -> int:
    #mixed implementation of Extended Euclidian and Modular inverse to get desired private key
    global q, r
    q = 0
    r = 1

    if (e == 0):
        return
 
    EEMI(n % e, e)
    q1, r1 = q, r
 
    q = r1 - (n // e) * q1
    r = q1

    if q < 1:
        return n + q
    else:
        return q

def RSA_encrypt(e: int, m: str, n: int) -> int:
    #simple encryption and int fudging for RSA
    byteM = bytes(m, 'utf-8')
    byteM = int.from_bytes(byteM, "big")
    
    return fastexp(byteM, e, n)

def RSA_decrypt(d: int, c: int, n: int) -> int:
    #simple decryption and bit fudging for RSA
    pText = fastexp(c, d, n)
    pText = pText.to_bytes((pText.bit_length() + 7) // 8, 'big') or b'\0'
    pText = bytes.decode(pText, "utf-8")
    return pText


if __name__ == "__main__":
    b = 4235880211405804673
    e = 131
    n = 12855544647099734480

    diffieCyper = "0dd055ab0934c23c43a2cd6865f1eac4165ff12f3a5db893222d204bf5b2b0408bb974695a67c8f5106640870974587414e40c03a9e68ab20c11cdd923b40e46f4458e0462d5c50fc5c679e59bd34edb4b8ef471a7c31366fbf6a0b5d529a0adf2b8d3a2075e914be060431ef6ae303b2ffa3f81b15e7faa2b96c33c53553a305cf4bc6061e91d57f33f90d41d97d87736f1358e7e17f7afa5e676e56ba4715cb64f82f902958f4916144c6180a6069cd2eb87158f36b91a0877fc9471c9b0256a0e7a45457eb29d18440a102d0860c600a8f4bad33aad5678f5f8cfc8d2a5681ee0fe3c22a424dcb2f00ba57ed8d2f1da60926a8bce27a64b414e19e67c70746e00571d326d30a75117ed5a649eadf95e5be95b7ee201b8bbd3f57d8fd2c2890e52e9d906665a642f7b5bb126f84394"
    iv = "0c7317295aae0c94fc5cafd21aab83da"

    modp = 140274374150807592491449133255658231264268770631566034386022222100531343719074131494320604278312778732859456385125624162933502046700948579578441334754582148485091680383613071507321333900217883755516757499505617257396578048774303326718471426859340410626824475827439545034654263158357112035471608065055234954703
    givenPublicKey = 129998305760875494303825127295381419744149154757555354724922666832177595998185089735243283967259471523111573189223611488039868561416920427510063820903942175531456159461230757807760091373036253390533191093697394825288432062185663971242161885062140820871427501585906394018803615889728291596555014352529771916952
    myPublicKey = 62388126366751748026464121063031780123793881612900982758396747429562855323952422308624492822470229538626629011504437233880514311313184432136219544434528842471212901942822283922862770797020908348195605718817002421689051394529315140222354246525501341101764847469064453976323082651519950819936975047753264520844
    myPrivateKey = 719710143204016798441011644845587099213677084916549512775742401128109990819513909575951350433270788947066904012767513838441469224481372303564996842694548176789745033823420127982804387273965038268678223333017219209284666690067778215484464109407771866005271979697982550239802927632425332339953954739051513275

    #res = fastexp(b, e, n)
    #tmp = millerR(175118011353974613747414115745586823026539540640072921440880723823673023327752553018161242200813211305556829955825029953131751251477020252777664395370693866564432656651061844109313776792589236703517908150685842487470642697808561061731352854662829518025487893728617216219673621722830025917527599882791614689407, 20)

    #x = primeGen(1024)
    #x = primeGen(1024)
    #print(x)

    #print(diffe_helman_pk(modp, 5))
    key = diffe_helman_decrypt(myPrivateKey, givenPublicKey, modp)
    AES_CBC(key, iv, diffieCyper)

    rsaE = 65537

    rsaD = 5360589253831810457948470021267803453091245236918644261185600874030875093026478030537108027308047828590558947455339042743300196125515405041266397808169000117007698888414055302741498305088771952569466175703781108863429203391170653352970213165707864485212975918547058167470967039500352538724600664437499217069673411697859440343304547032838616102794960569842697906296476410864031925889867930846042107980474220093385338534465109951396040129141907475913151569500546806271836654075375894721192025304453236431068748244485870142447840622247183970462060431999080493385541698420152505770408892645008278734712847956909130097313

    rsaN = 21468891342481994743496020519666831759058967189680835305873913742444479404282344823228455682332408368512555716168452385985557623654235095342793688166339022284791833417867999411865654755597827392785694497500531809556499615170322116157028163055548540379332852772782849616325150749678232970569185635861671118864580335504586855250974368136292953969211595242235046670269223686420409624332515421608505815520771554390825576561365808642411244926968281441956731813944088730402601677498813679405769031811964493128240525574254604232112695749184784113673972349866008696091269990384366628650969105754457749958088580579356441347139

    rsaM = "semimetamorphosis"

    rsaC = 1342890310358409814328467200358740005248005596173347793581166659831505834491333805939050604687306471521143225710332569555442418086173711229958717449971469746420757601327320587503769668598789029254034450398583724645792851155534176626732941935009646276659182459390561015131442091927060143899125168904238103526867033296928503591526349734818302900659891844197695420223014380898247918071206493167537202704199233705135515117582653486375882787282379185491516442483497017935188373302332353224701686247131841058902345544268601976043159460409632398792776262038481683789709488853244080747783284831636003906675314602446737690960

    #p, q = RSA_gen(1024)

    #print(p)
    #print(q)
    #n = p * q
    #print(n)

    #n1 = (p-1) * (q-1)
    #print(n1)

    #tmp = EEMI(65537, n1)
    #print(tmp)

    #crypt = RSA_encrypt(rsaE, rsaM, rsaN)
    #print(crypt)

    decrypt = RSA_decrypt(rsaD, rsaC, rsaN)
    print(decrypt)



    