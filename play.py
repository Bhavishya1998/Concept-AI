from state import X, O, BOARD_SIZE
from tree import Node
from tree_operations import next_node

from debug import print_board
from state_operations import empty_state

import random

def num_to_move(num: int):
    x = num % BOARD_SIZE
    y = num // BOARD_SIZE

    return x, y

def move_to_num(move):
    x, y = move
    return  y * BOARD_SIZE + x

def player_move(node: Node):

    if len(node.children) == 0:
        # TODO generate just the node needed?
        node.generate_children()

    # TODO Print available moves. Account for symmetry.
    # print("Available moves: ", end='')
    # for move in node.children.keys():
    #     print(move_to_num(move), end=' ')

    num = input("Enter cell: ")
    move = num_to_move(int(num))
    return next_node(node, move, pre_adjust_move=True)

def random_move(node: Node):
    return random.choice(list(node.children.keys()))

def ai_move(node: Node, rand=False):
    if rand:
        move = random_move(node)
    else:
        move = node.select_next()
    return next_node(node, move, pre_adjust_move=False)

def user_select_token():

    token = None
    while token is None:
        c = input("X/O? ")
        if c in ['X', 'x']:
            token = X
        elif c in ['O', 'o']:
            token = O

    return token

def game(random_first=False):
    def play(node: Node, rand: bool):

        print_board(node.state, flip_vertical=node.flip_vertical, flip_horizontal=node.flip_horizontal)

        if node.state.game_over():
            print("Game Over.\n")
            return
        
        if node.state.next_to_move == user_player:
            return play(player_move(node), rand=rand)
        else:
            return play(ai_move(node, rand=rand), rand=False)

    user_player = user_select_token()
    state = empty_state()
    node = Node(state)
    node.generate_subtree()

    play(node, rand=random_first)

if __name__ == "__main__":
    while True:
        game(random_first=True)
        print()