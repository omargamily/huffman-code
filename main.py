from bitstring import BitArray, Bits
from tree_node import Tree_Node
import os
import timeit


class HuffmanCode:
    def __init__(self):
        self.char_freq = {}
        self.copy = {}
        self.roots = []
        self.codemap = dict()

    # ------------------------------ compression ------------------------------
    # get frequencies
    def get_frequency(self, filename):
        f = open(filename, 'r')
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
        for i in range(8 - len(padded_bits.replace("0b", ""))):
            padded_bits = '0' + padded_bits

        d = Bits(bin=padded_bits).bin
        return bits.tobytes(), Bits(bin=padded_bits).tobytes()

    # write binary characters into file

    def compress(self, filename):
        text = self.get_frequency(filename)
        self.root_nodes()
        self.WalkTree(self.roots[0], '')
        print(self.codemap)
        text_bytes, padded_byte = self.encode(text)
        s = ''
        for key in self.codemap.keys():
            s = s + key + '\t' + self.codemap.get(key) + '\n'
        s = s + '--\n'
        open(filename.split('.')[0] + 'compressed.txt', 'w').write(s)
        open(filename.split('.')[0] +
             'compressed.txt', 'ab').write(padded_byte)
        open(filename.split('.')[0] +
             'compressed.txt', 'ab').write(text_bytes)
        print('compressed')

    def compress_folders(self, foldername):
        files_list = os.listdir(foldername)
        text = ''
        for file in files_list:
            text += self.get_frequency('./' + foldername + "/" + file)
        self.root_nodes()
        self.WalkTree(self.roots[0], '')
        print(self.codemap)
        s = ''
        for key in self.codemap.keys():
            s = s + key + '\t' + self.codemap.get(key) + '\n'
        s = s + '--\n'
        # print codemap
        open('folder compressed.txt', 'w').write(s)
        for file in files_list:
            f = open('./' + foldername + "/" + file, 'r')
            text1 = f.read()
            f.close()
            text_bytes, padded_byte = self.encode(text1)
            open('folder compressed.txt', 'a').write('-' + file + '-' + '\n')
            open('folder compressed.txt', 'ab').write(padded_byte)
            open('folder compressed.txt', 'ab').write(text_bytes)
            open('folder compressed.txt', 'a').write('\n--\n')
            text1 = ''
        print('compressed')

    # ----------------------decompression-------------------
    def decode(self, text):
        ans = ''
        i = n = 0
        print(len(text))
        while i in range(len(text)):
            partition = text[i:n]
            if self.codemap.get(partition) is not None:
                ans = ans + self.codemap.get(partition)
                i = n
            else:
                n += 1
        return ans

    # get code map and return line number where binary starts
    def get_codemap(self, filename):
        f = open(filename, 'r', errors='ignore')
        LineCounter = 0
        while True:
            line = f.readline()
            if line == '--\n':
                f.close()
                break
            else:
                if line != '\n':
                    var_code = line.rstrip('\n').split('\t')
                    self.codemap.update({var_code[1]: var_code[0]})
            LineCounter += 1
        print(self.codemap)
        return LineCounter

    def decompress(self, filename):
        linecounter = self.get_codemap(filename)
        text_array = ''

        # open text file and read as binary
        fp = open(filename, 'rb')
        for i, line in enumerate(fp):
            # start using binary data
            if i > linecounter:
                text_array = text_array + Bits(line).bin
        fp.close()

        # slicing padded bits
        padded = int(text_array[:8], 2)
        text_array = text_array[8:]
        if padded != 0:
            text_array = text_array[:-padded]
        open(filename.replace("compressed", "decompressed"), 'w').write(self.decode(text_array))

    def decompress_folders(self, filename):
        linecounter = self.get_codemap(filename)
        text_array = ''
        fp = open(filename, 'rb')
        os.makedirs('testdecompressed')
        for i, line in enumerate(fp):
            # start using binary data
            if i > linecounter:
                text_array = text_array + Bits(line).bin
                padded = int(text_array[:8], 2)
                text_array = text_array[8:]
                if padded != 0:
                    text_array = text_array[:-padded]
                open(filename.replace("compressed", "decompressed"), 'w').write(self.decode(text_array))

        fp.close()

    def compression_ratio(self):
        ratio = 0
        for key, value in self.char_freq.items():
            ratio += (len(self.codemap.get(key)) * int(value))
        return ratio / 8


if __name__ == '__main__':
    filename = input('enter filename')
    state = input('1-- compression\n2-- decompression\n3-- folder compression\n4-- folder decompress')
    hc = HuffmanCode()
    if state == '1':
        start = timeit.default_timer()
        hc.compress(filename)
        stop = timeit.default_timer()
        print('compression rate: ' + str(hc.compression_ratio()))
        print('time: ' +str(stop - start))
    if state == '2':
        start = timeit.default_timer()
        hc.decompress(filename)
        stop = timeit.default_timer()
        print('time: ' + str(stop - start))
    if state == '3':
        start = timeit.default_timer()
        hc.compress_folders(filename)
        stop = timeit.default_timer()
        print('time: ' + str(stop - start))
    if state == 4:
        start = timeit.default_timer()
        hc.decompress_folders(filename)
        stop = timeit.default_timer()
        print('time: ' + str(stop - start))
