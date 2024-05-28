class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.value = new_value

    def get_next_node(self):
        return self.next_node

    def set_next_node(self, new_node):
        self.next_node = new_node


class MyQueue:
    def __init__(self):
        self.amount = 0
        self.top = None

    def IsEmpty(self):
        return self.amount <= 0

    def Enqueue(self, node):
        if self.IsEmpty():
            self.top = node
        else:
            current = self.top
            while current.get_next_node() is not None:
                current = current.get_next_node()
            current.set_next_node(node)
        self.amount += 1

    def Dequeue(self):
        if self.IsEmpty():
            return None
        dequeued = self.top
        self.top = self.top.get_next_node()
        self.amount -= 1
        return dequeued

    def peek(self):
        if self.IsEmpty():
            return None
        return self.top.get_value()


a = Node(1)
b = Node(2)
c = Node(3)

queue = MyQueue()
queue.Enqueue(a)
queue.Enqueue(b)
queue.Enqueue(c)

print(queue.peek())
