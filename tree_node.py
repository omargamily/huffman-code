class Tree_Node:
    def __init__(self, letter=None, freq=None, left=None, right=None):
        self.letter = letter
        self.freq = freq
        self.right = right
        self.left = left

    def isleaf(self):
        if self.left is None and self.right is None:
            return True
        else:
            return False

    def __str__(self):
        return self.letter + " " + str(self.freq)
