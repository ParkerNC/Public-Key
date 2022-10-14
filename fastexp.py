from random import randrange

def fastexp(b: int, e: int, n: int) -> int:
    prod = 1
    base = b
    exp = bin(e)[::-1]
    for bit in exp:
        if bit == "1":
            prod = ((prod % n) * (base % n)) %n
        base = ((base % n) * (base % n)) %n

    return prod

def millerR(p: int, i: int) -> bool:
    s = 0
    n = p
    d = n-1
    while(d%2 == 0):
        s += 1
        d = d // 2

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

if __name__ == "__main__":
    b = 4235880211405804673
    e = 131
    n = 12855544647099734480

    #res = fastexp(b, e, n)
    tmp = millerR(175118011353974613747414115745586823026539540640072921440880723823673023327752553018161242200813211305556829955825029953131751251477020252777664395370693866564432656651061844109313776792589236703517908150685842487470642697808561061731352854662829518025487893728617216219673621722830025917527599882791614689407, 20)

    print(tmp)