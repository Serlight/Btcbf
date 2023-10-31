import requests
from bit import Key
from time import sleep, time
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
import hashlib


if os.path.exists(os.getcwd() + "/cache.txt") == False:
    open("cache.txt", "w+")


class Btcbf:
    def __init__(self):
        self.start_t = 0
        self.prev_n = 0
        self.cur_n = 0
        self.start_n = 0
        self.end_n = 0
        self.seq = False
        self.privateKey = None
        self.start_r = 0
        loaded_addresses = open("address09_2023.txt", "r").readlines()
        loaded_addresses = [x.rstrip() for x in loaded_addresses]
        # Remove invalid wallet addresses
        loaded_addresses = [
            x for x in loaded_addresses if x.find("wallet") == -1 and len(x) > 0
        ]
        self.loaded_addresses = set(loaded_addresses)

    def speed(self):
        while True:
            if self.cur_n != 0:
                cur_t = time()
                n = self.cur_n
                if self.prev_n == 0:
                    self.prev_n = n
                elapsed_t = cur_t - self.start_t
                print(
                    "current n: "
                    + str(n)
                    + ", current rate: "
                    + str(abs(n - self.prev_n) // 2)
                    + "/s"
                    + f", elapsed time: [{str(elapsed_t//3600)[:-2]}:{str(elapsed_t//60%60)[:-2]}:{int(elapsed_t%60)}], total: {n-self.start_r} ",
                    end="\r",
                )
                self.prev_n = n
                if self.seq:
                    open("cache.txt", "w").write(
                        f"{self.cur_n}-{self.start_r}-{self.end_n}"
                    )
            sleep(2)

    def random_brute(self, n):
        self.cur_n = n
        key = Key()
        native_segwig_address = self.get_bech32_address(key)
        nested_segwit_address = key.segwit_address
        address = key.address
        if address in self.loaded_addresses or native_segwig_address in self.loaded_addresses or nested_segwit_address in self.loaded_addresses:
            print("Wow matching address found!!")
            print("Public Adress: " + key.address)
            print("Private Key: " + key.to_wif())
            f = open(
                "foundkey.txt", "a"
            )  # the found privatekey and address saved to "foundkey.txt"
            f.write(key.address + "\n")
            f.write(key.to_wif() + "\n")
            f.close()
            sleep(510)
            exit()

    def sequential_brute(self, n):
        self.cur_n = n
        key = Key().from_int(n)
        native_segwig_address = self.get_bech32_address(key)
        nested_segwit_address = key.segwit_address
        address = key.address
        if address in self.loaded_addresses or native_segwig_address in self.loaded_addresses or nested_segwit_address in self.loaded_addresses:
            print("Wow matching address found!!")
            print("Public Adress: " + key.address)
            print("Private Key: " + key.to_wif())
            f = open(
                "foundkey.txt", "a"
            )  # the found privatekey and address saved to "foundkey.txt"
            f.write(key.address + "\n")
            f.write(key.to_wif() + "\n")
            f.close()
            sleep(500)
            exit()

    def random_online_brute(self, n):
        self.cur_n = n
        key = Key()
        the_page = requests.get(
            "https://blockchain.info/q/getreceivedbyaddress/" + key.address + "/"
        ).text
        if int(the_page) > 0:
            print(the_page)
            print("Wow active address found!!")
            print(key.address)
            print(key.to_wif())
            f = open(
                "foundkey.txt", "a"
            )  # the found privatekey and address saved to "foundkey.txt"
            f.write(key.address + "\n")
            f.write(key.to_wif() + "\n")
            f.close()
            sleep(500)
            exit()

    def num_of_cores(self):
        available_cores = cpu_count()
        cores = input(
            f"\nNumber of available cores: {available_cores}\n \n How many cores to be used? (leave empty to use all available cores) \n \n Type something>"
        )
        if cores == "":
            self.cores = int(available_cores)
        elif cores.isdigit():
            cores = int(cores)
            if 0 < cores <= available_cores:
                self.cores = cores
            elif cores <= 0:
                print(f"Hey you can't use {cores} number of cpu cores!!")
                input("Press Enter to exit")
                raise ValueError("negative number!")
            elif cores > available_cores:
                print(f"\n You only have {available_cores} cores")
                print(f" Are you sure you want to use {cores} cores?")
                core_input = input("\n[y]es or [n]o>")
                if core_input == "y":
                    self.cores = cores
                else:
                    print("using available number of cores")
                    self.cores = available_cores
        else:
            print("Wrong input!")
            input("Press Enter to exit")
            exit()

    def generate_random_address(self):
        key = Key()
        print("\n Public Address: " + key.address)
        print(" Private Key: " + key.to_wif())

    def generate_address_fromKey(self):
        if self.privateKey != "":
            key = Key(self.privateKey)
            print("\n Public Address: " + key.address)
            print("\n Your wallet is ready!")
        else:
            print("no entry")

    def get_user_input(self):
        user_input = input(
            "\n What do you want to do? \n \n   [1]: generate random key pair \n   [2]: generate public address from private key \n   [3]: brute force bitcoin offline mode \n   [4]: brute force bitcoin online mode \n   [0]: exit \n \n Type something>"
        )
        if user_input == "1":
            self.generate_random_address()
            print("\n Your wallet is ready!")
            input("\n Press Enter to exit")
            exit()
        elif user_input == "2":
            self.privateKey = input("\n Enter Private Key>")
            try:
                self.generate_address_fromKey()
            except:
                print("\n incorrect key format")
            input("Press Enter to exit")
            exit()
        elif user_input == "3":
            method_input = input(
                " \n Enter the desired number: \n \n   [1]: random attack \n   [2]: sequential attack \n   [0]: exit \n \n Type something>"
            )
            if method_input == "1":
                target = self.random_brute
            elif method_input == "2":
                if open("cache.txt", "r").read() != "":
                    r0 = open("cache.txt").read().split("-")
                    print(f"resume range {r0[0]}-{r0[2]}")
                    with ThreadPoolExecutor(max_workers=self.num_of_cores()) as pool:
                        print("\nResuming ...\n")
                        self.start_t = time()
                        self.start_r = int(r0[1])
                        self.start_n = int(r0[0])
                        self.end_n = int(r0[2])
                        self.seq = True
                        for i in range(self.start_n, self.end_n):
                            pool.submit(self.sequential_brute, i)
                        print("Stopping\n")
                        exit()
                else:
                    range0 = input("\n Enter range in decimals(example:1-100)>")
                    r0 = range0.split("-")
                    r0.insert(1, r0[0])
                    open("cache.txt", "w").write("-".join(r0))
                    with ThreadPoolExecutor(max_workers=self.num_of_cores()) as pool:
                        print("\n Starting ...")
                        self.start_t = time()
                        self.start_r = int(r0[1])
                        self.start_n = int(r0[0])
                        self.end_n = int(r0[2])
                        self.seq = True
                        for i in range(self.start_n, self.end_n):
                            pool.submit(self.sequential_brute, i)
                        print("Stopping\n")
                        exit()
            else:
                print("exitting...")
                exit()
        elif user_input == "4":
            method_input = input(
                " \n Enter the desired number: \n \n   [1]: random attack \n   [2]: sequential attack \n   [0]: exit \n \n Type something>"
            )
            if method_input == "1":
                with ThreadPoolExecutor(max_workers=self.num_of_cores()) as pool:
                    r = range(100000000000000000)
                    print("\n Starting ...")
                    self.start_t = time()
                    self.start_n = 0
                    for i in r:
                        pool.submit(self.random_online_brute, i)
                        sleep(0.1)
                    print("Stopping\n")
                    exit()
            elif method_input == "2":
                print("sequential online attack will be available soon!")
                input("Press Enter to exit")
                exit()
            else:
                print("exitting...")
                exit()
        elif user_input == "0":
            print("exitting")
            sleep(2)
            exit()
        else:
            print("No input. <1> chosen automatically")
            self.generate_random_address()
            print("Your wallet is ready!")
            input("Press Enter to exit")
            exit()
        with ThreadPoolExecutor(max_workers=self.num_of_cores()) as pool:
            r = range(100000000000000000)
            print("\n Starting ...")
            self.start_t = time()
            self.start_n = 0
            for i in r:
                pool.submit(target, i)
            print("Stopping\n")
            exit()

    def bech32_polymod(self, values):
        generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
        chk = 1
        for value in values:
            top = chk >> 25
            chk = (chk & 0x1FFFFFF) << 5 ^ value
            for i in range(5):
                chk ^= generator[i] if ((top >> i) & 1) else 0

        return chk


    def bech32_hrp_expand(self, hrp):
        return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


    def bech32_verify_checksum(self, hrp, data):
        return self.bech32_polymod(self.bech32_hrp_expand(hrp) + data) == 1


    def bech32_create_checksum(self, hrp, data):
        values = self.bech32_hrp_expand(hrp) + data
        polymod = self.bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
        return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


    CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

    def bech32_encode(self, hrp, data):
        combined = data + self.bech32_create_checksum(hrp, data)
        return hrp + "1" + "".join([self.CHARSET[d] for d in combined])

    def convertbits(self, data, frombits, tobits, pad=True):
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


    def bech32_decode(self, bech):
        if (any(ord(x) < 33 or ord(x) > 126 for x in bech)) or (
            bech.lower() != bech and bech.upper() != bech
        ):
            return (None, None)
        bech = bech.lower()
        pos = bech.rfind("1")
        if pos < 1 or pos + 7 > len(bech) or len(bech) > 90:
            return (None, None)
        if not all(x in self.CHARSET for x in bech[pos + 1 :]):
            return (None, None)
        hrp = bech[:pos]
        data = [self.CHARSET.find(x) for x in bech[pos + 1 :]]
        if not self.bech32_verify_checksum(hrp, data):
            return (None, None)
        return (hrp, data[:-6])


    def decode(self, hrp, addr):
        hrpgot, data = self.bech32_decode(addr)
        if hrpgot != hrp:
            return (None, None)
        decoded = self.convertbits(data[1:], 5, 8, False)
        if decoded is None or len(decoded) < 2 or len(decoded) > 40:
            return (None, None)
        if data[0] > 16:
            return (None, None)
        if data[0] == 0 and len(decoded) != 20 and len(decoded) != 32:
            return (None, None)
        return (data[0], decoded)


    def encode(self, hrp, witver, witprog):
        ret = self.bech32_encode(hrp, [witver] + self.convertbits(witprog, 8, 5))
        if self.decode(hrp, ret) == (None, None):
            return None
        return ret


    def get_bech32_address(self, key):
        sha256_1 = hashlib.sha256(key.public_key)
        ripemd160 = hashlib.new("ripemd160")
        ripemd160.update(sha256_1.digest())
        keyhash = ripemd160.digest()

        bech32 = self.encode("bc", 0, keyhash)
        # print("native address: " + bech32)
        return bech32

if __name__ == "__main__":
    obj = Btcbf()
    try:
        t0 = threading.Thread(target=obj.get_user_input)
        t1 = threading.Thread(target=obj.speed)
        t1.daemon = True
        t0.daemon = True
        t0.start()
        t1.start()
        sleep(4000000)  # stay in the `try..except`
        sleep(4000000)  # stay in the `try..except`
    except KeyboardInterrupt:
        print("\n\nCtrl+C pressed. \nexitting...")
        exit()
    else:
        print(f"\n\nError: {Exception.args}\n")
        exit()

