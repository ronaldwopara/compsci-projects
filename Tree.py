from collections import deque

from BFS import bfs


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def __str__(self):
        stack = deque()
        stack.append([self, 0])
        level_str = "\n"
        while len(stack) > 0:
            nod, level = stack.pop()

            if level > 0:
                level_str += "| " * (level - 1) + "|-"
            level_str += str(nod.value)
            level_str += "\n"
            level += 1
            for child in reversed(nod.children):
                stack.append([child, level])

        return level_str





sample_root_node = TreeNode("Home")
docs = TreeNode("Documents")
photos = TreeNode("Photos")
sample_root_node.children = [docs, photos]
my_wish = TreeNode("WishList.txt")
my_todo = TreeNode("TodoList.txt")
my_cat = TreeNode("Fluffy.jpg")
my_dog = TreeNode("Spot.jpg")
docs.children = [my_wish, my_todo]
photos.children = [my_cat, my_dog]

print(sample_root_node)
# Change the 2nd argument below
goal_path = bfs(sample_root_node, "Fluffy.jpg")
if goal_path is None:
    print("No path found")
else:
    print("Path found")
    for node in goal_path:
        print(node.value)
