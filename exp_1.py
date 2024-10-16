from hashlib import sha1
from base64 import b64decode
from Crypto.Cipher import AES

C = '9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI'
K = '12345678<8<<<1110182<111116?<<<<<<<<<<<<<<<4'


def pre(k):
    k = list(k)
    weights = [7, 3, 1, 7, 3, 1]
    sum = 0
    for i in range(21, 27):
        sum = (sum + int(k[i]) * weights[i - 21]) % 10
    k[27] = str(sum)
    return ''.join(k)


def getK_seed(k):
    mrz_imt = k[:10] + k[13:20] + k[21:28]
    H_SHA1 = sha1(mrz_imt.encode()).hexdigest()
    return H_SHA1[:32]


def getKab(k):
    kab = []
    k = '{:064b}'.format(int(k, 16))
    for i in range(0, len(k), 8):
        kab.append(k[i:i + 7])
        if k[i:i + 7].count('1') % 2 == 0:
            kab.append('1')
        else:
            kab.append('0')
    return hex(int(''.join(kab), 2))[2:]


def getKey(k):
    k = k + '00000001'
    H = sha1(bytes.fromhex(k)).hexdigest()
    return getKab(H[:16]) + getKab(H[16:32])

def getP(C, k):
    C = b64decode(C)
    aes =  AES.new(bytes.fromhex(k), AES.MODE_CBC, bytes.fromhex('0'*32))
    return aes.decrypt(C).decode()

if __name__ == '__main__':
    K = pre(K)
    K_seed = getK_seed(K)
    Key = getKey(K_seed)
    P = getP(C, Key)
    print(P)