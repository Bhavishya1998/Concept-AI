from state import State, X, O, EMPTY
from tree import Node

class IllegalMoveException(Exception):
    pass

def next_node(node: Node, move):
    """  """

    # move adjusted for reflections
    adjusted_move = move

    if node.flip_horizontal:
        adjusted_move = node.state._reflection_in_horizontal(adjusted_move)
    if node.flip_vertical:
        adjusted_move = node.state._reflection_in_vertical(adjusted_move)

    if adjusted_move in node.children:
        child_node = node.children[adjusted_move]
        child_node.flip_horizontal = node.flip_horizontal 
        child_node.flip_vertical = node.flip_vertical 
        return node.children[adjusted_move]
    elif node.state.horizontal_symmetry and node.state._reflection_in_horizontal(adjusted_move) in node.children:
        adjusted_move = node.state._reflection_in_horizontal(adjusted_move)
        child_node = node.children[adjusted_move]
        child_node.flip_horizontal = not node.flip_horizontal
        child_node.flip_vertical = node.flip_vertical 
        return node.children[adjusted_move]
    elif node.state.vertical_symmetry and node.state._reflection_in_vertical(adjusted_move) in node.children:
        adjusted_move = node.state._reflection_in_vertical(adjusted_move)
        child_node = node.children[adjusted_move]
        child_node.flip_horizontal = node.flip_horizontal
        child_node.flip_vertical = not node.flip_vertical 
        return node.children[adjusted_move]
    elif node.state.horizontal_symmetry and node.state.vertical_symmetry and \
         node.state._reflection_in_horizontal(node.state._reflection_in_vertical(adjusted_move)) in node.children:
        
        adjusted_move = node.state._reflection_in_horizontal(node.state._reflection_in_vertical(adjusted_move))
        child_node = node.children[adjusted_move]
        child_node.flip_horizontal = not node.flip_horizontal
        child_node.flip_vertical = not node.flip_vertical 
        return node.children[adjusted_move]
    else:
        # NOTE should I???
        raise IllegalMoveException
