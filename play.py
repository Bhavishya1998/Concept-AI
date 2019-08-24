from state import X, O
from tree import Node
from tree_operations import next_node

from debug import print_board
from state_operations import empty_state

def player_move(node: Node):

    if len(node.children) == 0:
        # TODO generate just the node needed?
        node.generate_children()
        
    cell = input("Enter cell: ")
    y, x = tuple([int(coord) for coord in cell.split(" ")])
    return next_node(node, (x, y), pre_adjust_move=True)

def ai_move(node: Node):
    move = node.select_next()
    return next_node(node, move, pre_adjust_move=False)

def user_select_token():

    # TODO complete
    return X

def game():
    def play(node: Node):

        print_board(node.state, flip_vertical=node.flip_vertical, flip_horizontal=node.flip_horizontal)

        if node.state.game_over():
            print("Game Over.")
            return
        
        if node.state.next_to_move == user_token:
            return play(player_move(node))
        else:
            return play(ai_move(node))

    user_token = user_select_token()
    state = empty_state()
    node = Node(state)
    node.generate_subtree()

    play(node)

if __name__ == "__main__":
    game()