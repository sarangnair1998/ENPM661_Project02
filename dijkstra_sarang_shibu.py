import time
import copy
import cv2
from queue import PriorityQueue
import numpy as np
from math import cos, sin, pi


def action_move_up(node, canvas):
    return move_node(node, canvas, 0, -1)

def action_move_down(node, canvas):
    return move_node(node, canvas, 0, 1)

def action_move_right(node, canvas):
    return move_node(node, canvas, 1, 0)

def action_move_left(node, canvas):
    return move_node(node, canvas, -1, 0)

def action_move_up_right(node, canvas):
    return move_node(node, canvas, 1, -1)

def action_move_down_right(node, canvas):
    return move_node(node, canvas, 1, 1)

def action_move_down_left(node, canvas):
    return move_node(node, canvas, -1, 1)

def action_move_up_left(node, canvas):
    return move_node(node, canvas, -1, -1)


def valid(node, canvas, xdot, ydot):
    x, y = node
    new_x, new_y = x + xdot, y + ydot
    return (0 <= new_x < canvas.shape[1] and 0 <= new_y < canvas.shape[0] 
            and canvas[new_y][new_x][2] < 255)

def move_node(node, canvas, xdot, ydot):
    next_node = (node[0] + xdot, node[1] + ydot)
    if valid(node, canvas, xdot, ydot):
        return True, next_node
    else:
        return False, node