from bitstring import BitArray, Bits
from tree_node import Tree_Node


class HuffmanCode:
    def __init__(self, filename):
        self.char_freq = {}
        self.copy = {}
        self.roots = []
        self.codemap = dict()
        self.filename = filename

    # ------------------------------ compression ------------------------------
    # get frequencies
    def get_frequency(self):
        f = open(self.filename + ".txt", 'r')
        text = f.read()
        for letter in text:
            if letter in self.char_freq.keys():
                num_times = self.char_freq.get(letter) + 1
                self.char_freq.update({letter: num_times})
            else:
                self.char_freq.update({letter: 1})
        return text

    def get_least_freq(self):
        letter = min(self.copy, key=self.copy.get)
        freq = self.copy.get(letter)
        del (self.copy[letter])
        return letter, freq
    # used for objects

    def extract_min(self):
        min = self.roots[0]
        for node in self.roots:
            if node.freq < min.freq:
                min = node
        return min
    # create tree

    def root_nodes(self):
        self.copy = self.char_freq.copy()
        # create root nodes for every character
        for i in range(len(self.copy.values())):
            letter, freq = self.get_least_freq()
            self.roots.append(Tree_Node(letter=letter, freq=freq))

        for i in range(len(self.roots) - 1):
            l1 = self.extract_min()
            self.roots.remove(l1)
            l2 = self.extract_min()
            self.roots.remove(l2)
            self.roots.append(Tree_Node(freq=int(l1.freq) +
                                        int(l2.freq), left=l1, right=l2))
    # create codemap

    def WalkTree(self, node, prefix):
        if node.isleaf():
            self.codemap.update({node.letter: prefix})
            prefix = ''
            return
        else:
            self.WalkTree(node.left, prefix + '0')
            self.WalkTree(node.right, prefix + '1')
    # convert characters into binary string

    def encode(self, text):
        bits = BitArray()
        for letter in text:
            bits.append(Bits(bin=self.codemap.get(letter)))
        if len(bits.bin) % 8 != 0:
            padded_bits = str(bin(8 - (len(bits.bin) % 8)))
        else:
            padded_bits = '0'
        while len(padded_bits.replace("b", "")) % 8 != 0:
            padded_bits = '0' + padded_bits
        return bits.tobytes(), Bits(bin=padded_bits).tobytes()
    # write binary characters into file

    def compress(self):
        text = self.get_frequency()
        self.root_nodes()
        self.WalkTree(self.roots[0], '')
        text_bytes, padded_byte = self.encode(text)
        s = ''
        for key in self.codemap.keys():
            s = s + key+'\t'+self.codemap.get(key)+'\n'
        s = s + '--\n'
        open(self.filename.split('.')[0] + 'output.txt', 'w').write(s)
        open(self.filename.split('.')[0] +
             'output.txt', 'ab').write(padded_byte)
        open(self.filename.split('.')[0] +
             'output.txt', 'ab').write(text_bytes)
        print('compressed')
    # -------------------- decompression -------------------

    def decode(self, text):
        # root node
        ans = ''
        node = self.roots[0]
        for i in text:
            if i is '0':
                node = node.left
            else:
                node = node.right
            if node.isleaf():
                ans = ans + node.letter
                node = self.roots[0]
        return ans

    def decompress(self):
        f = open('testoutput.txt', 'r')
        while True:
            line = f.readline()
            if line == '--\n':
                f.close()
                break
            else:
                var_code = line.rstrip('\n').split('\t')
                self.codemap.update({var_code[0]: var_code[1]})
        f.close()
        '''
        with open('dwn.txt') as f:
            for i in xrange(6):
                f.next()
            for line in f:
                process(line)
        f = open(self.filename + 'output.txt', 'rb')
        text_array = Bits(f.read()).bin
        padded = int(text_array[:8], 2)
        text_array = text_array[8:]
        if padded != 0:
            text_array = text_array[:-padded]
        print(self.decode(text_array))
        '''

if __name__ == '__main__':
    hc = HuffmanCode('sample')
    hc.compress()
   # hc.decompress()
