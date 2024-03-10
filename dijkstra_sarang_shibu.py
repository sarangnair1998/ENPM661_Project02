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
    
def draw_regular_polygon_with_clearance(canvas, color, vertex_count, radius, position, rotation=0, clearance=0,thickness = -1):
    n = vertex_count
    r = radius + clearance 
    x, y = position
    rotation_rad = pi / 180 * rotation 

    vertices = []
    for i in range(n):
        x_i = x + r * cos(rotation_rad + 2 * pi * i / n)
        y_i = y + r * sin(rotation_rad + 2 * pi * i / n)
        vertices.append((int(x_i), int(y_i)))
    
    return vertices

def obstacles_map(canvas):
    
    cv2.polylines(canvas, [np.array([(0, 0), (1200, 0), (1200, 500), (0, 500)])], isClosed=True, color=(0, 0, 255), thickness=5)
    
    cv2.fillPoly(canvas, pts = [np.array([(100,400), (175,400), (175,0), (100,0)])], color = (255, 0, 0))
    cv2.polylines(canvas, pts = [np.array([(100,400), (175,400), (175,0), (100,0)])],isClosed=True, color=(0, 0, 255), thickness=5)
    
    cv2.fillPoly(canvas, pts = [np.array([(275,100), (350,100), (350,500), (275,500)])], color = (255, 0, 0))
    cv2.polylines(canvas, pts = [np.array([(275,100), (350,100), (350,500), (275,500)])],isClosed=True, color=(0, 0, 255), thickness=5)
    
    hexagon1_center = (650, 250)
    hexagon1_radius = 150
    hexagon1_rotation = 90
    clearance1 = 0
    clearance2 = 5
    vertices1 = draw_regular_polygon_with_clearance(canvas, (0, 0, 255), 6, hexagon1_radius, hexagon1_center, hexagon1_rotation, clearance1)
    vertices2 = draw_regular_polygon_with_clearance(canvas, (0, 0, 255), 6, hexagon1_radius, hexagon1_center, hexagon1_rotation, clearance2)
    cv2.fillPoly(canvas, pts = [np.array(vertices1)], color = (255, 0, 0))
    cv2.polylines(canvas, pts = [np.array(vertices2)],isClosed=True, color=(0, 0, 255), thickness=5)
    
    cv2.fillPoly(canvas, pts = [np.array([(900,375), (1020,375), (1020,125), (900,125),(900,50),(1100,50),
                                          (1100,450),(900,450)])], color = (255, 0, 0))
    cv2.polylines(canvas, pts = [np.array([(900,375), (1020,375), (1020,125), (900,125),(900,50),(1100,50),
                                          (1100,450),(900,450)])],isClosed=True, color=(0, 0, 255), thickness=5)
    
    return canvas

