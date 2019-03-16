from Crypto import Random
import ecdh
import aes
import hashlib
from BloomFilter import BloomFilter

class PEKSClient:
    def KeyGen(self):
        rec_priv_key, rec_pub_key = ecdh.make_keypair()
        return rec_priv_key, rec_pub_key

    def PEKS(self, A_Pub, word):
        sen_priv_key, sen_pub_key = ecdh.make_keypair()
        s2 = ecdh.scalar_mult(sen_priv_key, A_Pub)
        hashGen = hashlib.sha256()
        hashGen.update(str(s2[0]).encode())
        hash = hashGen.hexdigest()

        M = Random.new().read(3)
        x = aes.encrypt(M, hash[:32])
        return sen_pub_key, x, M

    def Trapdoor(self, A_Priv, B_Pub, word):
        s1 = ecdh.scalar_mult(A_Priv, B_Pub)
        return s1


class PEKSServer:
    def __init__(self, key):
        self.key = key

    def Test(self, ciphers, M):
        hashGen = hashlib.sha256()
        hashGen.update(str(self.key[0]).encode())
        hash = hashGen.hexdigest()

        for cipher in ciphers:
            aes.decrypt(cipher, hash[:32])
            if(M == aes.decrypt(cipher, hash[:32])):
                print('yes')

class BloomFilterSearch():
    def __init__(self, ciphers_dict, bit_vec, hash):
        self.ciphers_dict = ciphers_dict
        self.bit_vec = bit_vec
        self.hash = hash
        self.false_positives = 0
        self.filter = BloomFilter(self.bit_vec, self.hash)

    def SearchWord(self, dictionary, word):
        server = PEKSServer(dictionary[word][0])
        server.Test(self.ciphers_dict, dictionary[word][1])

    def insert(self, s1, cipher):
        hashGen = hashlib.sha256()
        hashGen.update(str(s1[0]).encode())
        hash = hashGen.hexdigest()
        self.filter.insert(str(aes.decrypt(cipher, hash[:32])))

    def percentage(self, part, whole):
        return 100 * float(part) / float(whole)

    def bl_search(self, dict, store):
        for w in dict:
            result = self.filter.check(str(dict[w][1]))
            if (result is True):
                if(w not in store):
                    self.false_positives += 1

        p = self.percentage(self.false_positives, len(store))
        percent.append(p)
        o.write('Size of bit vector: '+ str(self.bit_vec) + '\n')
        o.write('Number of hashes used: ' + str(self.hash) + '\n')
        o.write('Number of false positives: ' + str(self.false_positives) + '\n')
        o.write('Percentage of false positives: ' + str(p) + '% \n\n\n')

if __name__ == '__main__':
    keys = []
    keyword_dict = {}
    ciphers = []
    bloom_keys = []
    store = []
    key_file = 'keywords.txt'
    stored_keys = 'keywords_stored.txt'
    out = 'result.txt'
    o = open(out, 'w')
    percent = []

    with open(key_file, 'r') as f:
        for line in f.readlines():
            keyword_dict[line.strip()] = []

    with open(stored_keys, 'r') as f:
        for line in f.readlines():
            store.append(line.strip())

    for word in keyword_dict:
        client = PEKSClient()
        priv, pub = client.KeyGen()
        s_pub, cipher, rM = client.PEKS(pub, word)
        s1 = client.Trapdoor(priv, s_pub, cipher)
        keyword_dict[word].append(s1)
        keyword_dict[word].append(rM)
        if (word in store):         # Only a subset of the keywords
            ciphers.append(cipher)  # are are present in the server
            bloom_keys.append(s1)

    vector = 50
    vectors = []
    o.write('Search Complete.\n\nResult:\nStored Keywords: ')
    for i in range(len(store)):
        if (i == len(store) - 1):
            o.write(str(store[i]) + '.\nNo of stored words: ' + str(i + 1) + '\n\n')
            continue
        o.write(str(store[i]) + ', ')
    for i in range(30):
        vectors.append(vector)
        search = BloomFilterSearch(ciphers, vector, 10)
        for i in range(len(ciphers)):
            search.insert(bloom_keys[i], ciphers[i])
        search.bl_search(keyword_dict, store)
        vector += 50
    o.close()


import matplotlib.pyplot as plt
x_val = percent
y_val = vectors

plt.plot(x_val, y_val)
plt.title('Hash size is constant')
plt.ylabel('Bit Vector Size')
plt.xlabel('False Positive Probability')

plt.legend()
plt.show()

# x_val = percent
# y_val = hashes
#
# plt.plot(x_val, y_val)
# plt.title('Bit Vector is Constant')
# plt.ylabel('Number of Hash Funtions')
# plt.xlabel('False Positive Probability')
#
# plt.legend()
# plt.show()
