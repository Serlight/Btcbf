from mnemonic import Mnemonic
import bip32utils
from bit import Key
from bit import PrivateKey
import hashlib

mnemon = Mnemonic("english")
# words = mnemon.generate(256)
# print(words)
# mnemon.check(words)
# seed = mnemon.to_seed(words)
phrase = b"april parent life merge river frog auto foot captain midnight under mango"
phrase1 = (
    b"elegant such check turkey genuine popular pact grant sister lend seed divert"
)
phrase2 = b"slogan brush favorite pole climb other ill sudden mask bounce miracle hello"


def checkWallet(phrase):
    seed = mnemon.to_seed(phrase)
    print(f"BIP39 Seed: {seed.hex()}\n")

    root_key = bip32utils.BIP32Key.fromEntropy(seed)
    P2WPKHoP2SHAddress = root_key.P2WPKHoP2SHAddress()
    root_address = root_key.Address()
    root_public_hex = root_key.PublicKey().hex()
    root_private_wif = root_key.WalletImportFormat()
    print("Root key:")
    print(f"\t(P2WPKHoP2SHAddress: {P2WPKHoP2SHAddress})")
    print(f"\tAddress: {root_address}")
    print(f"\tPublic : {root_public_hex}")
    print(f"\tPrivate: {root_private_wif}\n")

    child_key = root_key.ChildKey(0).ChildKey(0)
    child_address = child_key.Address()
    child_public_hex = child_key.PublicKey().hex()
    child_private_wif = child_key.WalletImportFormat()
    print("Child key m/0/0:")
    print(f"\tAddress: {child_address}")
    print(f"\tPublic : {child_public_hex}")
    print(f"\tPrivate: {child_private_wif}\n")


def checkWalletFromPrivateKey(key):
    k = PrivateKey(wif=key)
    b = k.get_balance
    print(f"wallet balance {b}")

    pass


p1 = "L4uKjbX6tYMqVoBpHQ77jvq4FQvrkfW15U3ZKkh3Yf5qcYXkZtK4"
p2 = "L4g8E4PajMRc4vGkHfd7VQ2TJGyANbr9E53z2yyKiRkTP9ZFzPDq"
p3 = "L4uKjbX6tYMqVoBpHQ77jvq4FQvrkfW15U3ZKkh3Yf5qcYXkZtK4"
p4 = "L3m13gS87DNZ1b3mtEaDJQDc4HtRjsfj8hGnULeKhsEBep4bczii"

for p in [p1, p2, p3, p4]:
    checkWalletFromPrivateKey(p)

import hashlib

def bech32_polymod(values):
    generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0

    return chk


def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_verify_checksum(hrp, data):
    return bech32_polymod(bech32_hrp_expand(hrp) + data) == 1


def bech32_create_checksum(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def bech32_encode(hrp, data):
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + "1" + "".join([CHARSET[d] for d in combined])


def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc) << frombits | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret


def bech32_decode(bech):
    if (any(ord(x) < 33 or ord(x) > 126 for x in bech)) or (
        bech.lower() != bech and bech.upper() != bech
    ):
        return (None, None)
    bech = bech.lower()
    pos = bech.rfind("1")
    if pos < 1 or pos + 7 > len(bech) or len(bech) > 90:
        return (None, None)
    if not all(x in CHARSET for x in bech[pos + 1 :]):
        return (None, None)
    hrp = bech[:pos]
    data = [CHARSET.find(x) for x in bech[pos + 1 :]]
    if not bech32_verify_checksum(hrp, data):
        return (None, None)
    return (hrp, data[:-6])


def decode(hrp, addr):
    hrpgot, data = bech32_decode(addr)
    if hrpgot != hrp:
        return (None, None)
    decoded = convertbits(data[1:], 5, 8, False)
    if decoded is None or len(decoded) < 2 or len(decoded) > 40:
        return (None, None)
    if data[0] > 16:
        return (None, None)
    if data[0] == 0 and len(decoded) != 20 and len(decoded) != 32:
        return (None, None)
    return (data[0], decoded)


def encode(hrp, witver, witprog):
    ret = bech32_encode(hrp, [witver] + convertbits(witprog, 8, 5))
    if decode(hrp, ret) == (None, None):
        return None
    return ret


def get_bech32_address():
    key = Key()
    sha256_1 = hashlib.sha256(key.public_key)
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(sha256_1.digest())
    keyhash = ripemd160.digest()

    bech32 = encode("bc", 0, keyhash)
    print("native address: " + bech32)


get_bech32_address()


# checkWalletFromPrivateKey(p1)
# checkWallet('stomach pear woman genuine wave soldier gun include power tunnel bread mountain')
# checkWallet(phrase1)
# checkWallet(phrase2)
