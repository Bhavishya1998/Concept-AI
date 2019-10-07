from tree import Node
from state_operations import move, empty_state
from debug import print_tree

if __name__ == "__main__":
    state = move(move(move(move(move(move(move(move(move(empty_state(), 1), 2), 0), 1), 0), 0), 3), 6), 3)

    node = Node(state)
    node.create_subtree(2)

    print_tree(node)