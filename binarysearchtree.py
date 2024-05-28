class BinarySearchTree:
    def __init__(self, value, depth=1):
        self.value = value
        self.depth = depth
        self.left = None
        self.right = None

    # Define .insert() below:
    def insert(self, value):
        if value < self.value:
            if self.left is None:
                self.left = BinarySearchTree(value, self.depth + 1)
                print(f'Tree node {value} added to the left of {self.value} at depth {self.depth + 1}')
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = BinarySearchTree(value, self.depth + 1)
                print(f'Tree node {value} added to the right of {self.value} at depth {self.depth + 1}')
            else:
                self.right.insert(value)

    def get_node_children(self, value):
        if (value == self.value) and (self.right or self.left is not None):
            return [self.right.value, self.left.value]
        elif (self.left is not None) and (value < self.value):
            return self.left.get_node_children(value)

        elif (self.left is not None) and (value > self.value):
            return self.right.get_node_children(value)

        else:
            return "No Children Found"

    def depth_first_traversal(self):
        if self.left is not None:
            self.left.depth_first_traversal()
        print(f'Depth={self.depth}, Value={self.value}')
        if self.right is not None:
            self.right.depth_first_traversal()


tree = BinarySearchTree(48)
tree.insert(24)
tree.insert(55)
tree.insert(26)
tree.insert(38)
tree.insert(56)
tree.insert(74)

# Print depth-first traversal:
tree.depth_first_traversal()

# Insert values below:
# root = BinarySearchTree(100)

# root.insert(50)
# root.insert(125)
# root.insert(75)
# root.insert(25)
#
# print(root.get_node_children(75))
