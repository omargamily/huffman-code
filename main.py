from tree_node import Tree_Node
import bitstring


class HuffmanCode:
    def __init__(self,filename):
        self.char_freq = {}
        self.copy = {}
        self.roots = []
        self.codemap = dict()
        self.filename = filename

    # get frequencies
    def get_frequency(self):
        f = open(self.filename+ ".txt", 'r')
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
            self.roots.append(Tree_Node(freq=int(l1.freq) + int(l2.freq), left=l1, right=l2))
    # create codemap
    def WalkTree(self,node,prefix):
        if node.isleaf():
            self.codemap.update({node.letter: prefix})
            prefix = ''
            return
        else:
            self.WalkTree(node.left, prefix + '0')
            self.WalkTree(node.right, prefix + '1')


# convert letters into code
    #convert charcaters into binary string
    def encode(self,text):
        return ''.join(self.codemap.get(letter) for letter in text)
    def compress(self):
        text = self.get_frequency()
        print(self.char_freq, '\n')
        self.root_nodes()
        self.WalkTree(self.roots[0], '')
        print(self.codemap)
        output_bytes = bitstring.Bits(bin=self.encode(text)).tobytes()
        open('output.txt', 'wb').write(output_bytes)

if __name__ == '__main__':
    hc = HuffmanCode('sample')
    hc.compress()
